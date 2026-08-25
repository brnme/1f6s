#!/usr/bin/env bash
# 1f6s.sh —— 把给定视频用 ffmpeg 转成符合「1帧6秒」八级压缩规范的输出
#
# 用法: 1f6s.sh <输入视频> [级别L1-L8] [选项]
#   级别默认 L4(倡议默认推荐)
#   默认输出: <basename>_1f6s.mp4(与源同目录),不覆盖原视频,不覆盖已存在输出
#
# 选项:
#   -o, --output <路径>    自定义输出文件名/路径
#   -y, --yes              跳过确认,直接执行
#   -n, --dry-run          只打印将执行的命令,不执行
#   -l, --list             打印八级参数速查表后退出
#   --target <MB>          L7 指定目标体积(MB),自动算视频码率(也可用于其他级别的 2-Pass)
#   --force                允许覆盖已存在的输出文件
#   -h, --help             显示帮助
#
# 参数真相源: 同目录 levels.json(脚本与 agent 共用,避免参数漂移)
# 依赖: ffmpeg + ffprobe(必装); jq(可选,缺失时用 python3 降级解析 JSON)
set -euo pipefail

# ---------- 定位 levels.json ----------
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
LEVELS_FILE="$SCRIPT_DIR/levels.json"

# ---------- 颜色输出(可关闭) ----------
if [ -t 1 ]; then
  C_BOLD=$'\033[1m'; C_CYAN=$'\033[36m'; C_YEL=$'\033[33m'; C_RED=$'\033[31m'; C_GRN=$'\033[32m'; C_DIM=$'\033[2m'; C_OFF=$'\033[0m'
else
  C_BOLD=''; C_CYAN=''; C_YEL=''; C_RED=''; C_GRN=''; C_DIM=''; C_OFF=''
fi
say()    { printf '%s\n' "$*"; }
notice() { printf '%s%s%s\n' "$C_CYAN" "$*" "$C_OFF" >&2; }
warn()   { printf '%s%s%s\n' "$C_YEL" "$*" "$C_OFF" >&2; }
err()    { printf '%s%s%s\n' "$C_RED" "$*" "$C_OFF" >&2; }
ok()     { printf '%s%s%s\n' "$C_GRN" "$*" "$C_OFF" >&2; }

# ---------- 帮助 ----------
usage() {
  cat <<'EOF'
1f6s.sh —— 用 ffmpeg 把视频转成符合「1帧6秒」八级压缩规范的输出

用法:
  1f6s.sh <输入视频> [级别] [选项]
  1f6s.sh -l, --list        打印八级参数速查表
  1f6s.sh -h, --help        显示本帮助

级别: L1 ~ L8(默认 L4)
  L1 标准级       1帧/6秒 480p 彩色 CRF32
  L2 黑白级       1帧/6秒 480p 黑白 CRF32
  L3 高压缩级     1帧/6秒 480p 黑白 CRF34
  L4 智能调优级   1帧/6秒 480p 黑白 CRF34 stillimage  ★ 默认推荐
  L5 音频极限级   1帧/6秒 480p 黑白 CRF34 stillimage 8k音频
  L6 长间隔级     1帧/10秒 360p 黑白 CRF36 stillimage 8k音频
  L7 2-Pass级     1帧/10秒 360p 黑白 2-Pass 精确体积(配 --target)
  L8 H.265极限级  1帧/10秒 360p 黑白 CRF38 keyint=1(需播放器支持 H.265)

选项:
  -o, --output <路径>   自定义输出文件名/路径
  -y, --yes             跳过确认,直接执行
  -n, --dry-run         只打印将执行的命令,不执行
  -l, --list            打印八级速查表后退出
  --target <MB>         L7 目标体积(MB),自动算视频码率
  --force               允许覆盖已存在的输出文件
  -h, --help            显示本帮助

默认输出: <basename>_1f6s.mp4(与源同目录),不覆盖原视频与已有文件。
EOF
}

# ---------- JSON 解析(优先 jq,降级 python3) ----------
json_field() {
  # json_field <json> <jq表达式>
  local json="$1" expr="$2"
  if command -v jq >/dev/null 2>&1; then
    jq -r "$expr" <<<"$json"
  elif command -v python3 >/dev/null 2>&1; then
    python3 -c "
import json,sys,re
d=json.loads(sys.argv[1])
expr=sys.argv[2].strip()
# 健壮的 jq 子集求值器,支持:
#   .a.b.c        链式字段(前导点可选)
#   .a[i]         数组下标
#   .a | length   管道
#   .levels[]     数组展开(返回 list)
#   .levels[] | .id   展开后取字段
#   .levels[i].id     展开下标再取字段
def tokenize(p):
    p=p.strip()
    if p.startswith('.'): p=p[1:]
    return p
def apply_part(o,p):
    p=tokenize(p)
    if p=='' : return o
    if p=='length': return len(o)
    if p=='empty': return None
    out=o
    # 拆成 字段 / [i] / [] 片段依次应用
    for seg in re.findall(r'[^.\[\]]+|\[\]|\[\d+\]', p):
        if seg=='[]':
            out=out            # 标记展开:返回 list 本身
            out=list(out) if not isinstance(out,list) else out
            # 展开本身不改变 out,由调用方处理;这里直接返回 list
            return out
        elif seg.startswith('[') and seg.endswith(']'):
            idx=int(seg[1:-1])
            out=out[idx]
        else:
            if isinstance(out,list):
                out=[x.get(seg) for x in out if isinstance(x,dict)]
                return out
            out=out[seg] if isinstance(out,dict) else getattr(out,seg,None)
    return out
def evaluate(root, e):
    # 按管道拆分
    parts=[x.strip() for x in e.split('|')]
    cur=root
    for part in parts:
        cur=apply_part(cur,part)
    return cur
v=evaluate(d,expr)
def emit(v):
    if isinstance(v,bool): print('true' if v else 'false')
    elif isinstance(v,list):
        for x in v:
            if x is None: print('')
            elif isinstance(x,bool): print('true' if x else 'false')
            else: print(x)
    elif v is None: print('null')
    else: print(v)
emit(v)
" "$json" "$expr"
  else
    err "需要 jq 或 python3 来解析 levels.json,二者均未找到。"
    exit 2
  fi
}

# ---------- 读取某级别参数 ----------
level_json() {
  # level_json <Lid> -> 该级别对象 JSON
  local lid="$1"
  if command -v jq >/dev/null 2>&1; then
    jq -e --arg id "$lid" '.levels[] | select(.id==$id)' "$LEVELS_FILE"
  elif command -v python3 >/dev/null 2>&1; then
    python3 -c "
import json,sys
d=json.load(open(sys.argv[1]))
lid=sys.argv[2]
for l in d['levels']:
    if l['id']==lid:
        print(json.dumps(l,ensure_ascii=False)); sys.exit(0)
sys.exit(1)
" "$LEVELS_FILE" "$lid"
  else
    err "需要 jq 或 python3 来解析 levels.json,二者均未找到。"
    exit 2
  fi
}

# ---------- 八级速查表 ----------
print_list() {
  if [ ! -f "$LEVELS_FILE" ]; then err "找不到 levels.json: $LEVELS_FILE"; exit 2; fi
  printf '%s%s1帧6秒 · 八级压缩速查表%s\n\n' "$C_BOLD" "$C_CYAN" "$C_OFF"
  printf '%-4s %-16s %-10s %-8s %-6s %-8s %-12s %s\n' "级别" "名称" "抽帧" "分辨率" "色彩" "质量" "音频" "预期体积(99min)"
  printf '%-4s %-16s %-10s %-8s %-6s %-8s %-12s %s\n' "----" "----------------" "----------" "--------" "------" "--------" "------------" "----------------"
  local all
  all="$(cat "$LEVELS_FILE")"
  local n i id name interval scale color codec crf abit tune twopass expsz extra
  n="$(json_field "$all" '.levels | length')"
  for ((i=0; i<n; i++)); do
    id="$(json_field "$all" ".levels[$i].id")"
    name="$(json_field "$all" ".levels[$i].name")"
    interval="$(json_field "$all" ".levels[$i].interval")"
    scale="$(json_field "$all" ".levels[$i].scale")"
    color="$(json_field "$all" ".levels[$i].color")"
    crf="$(json_field "$all" ".levels[$i].crf")"
    abit="$(json_field "$all" ".levels[$i].audio_bitrate")"
    twopass="$(json_field "$all" ".levels[$i].twopass")"
    expsz="$(json_field "$all" ".levels[$i].expected_size")"
    [ "$color" = "color" ] && color="彩色" || color="黑白"
    local fps="1帧/6秒"; [ "$interval" = "1/10" ] && fps="1帧/10秒"
    local res="480p"; [ "$scale" = "-2:360" ] && res="360p"
    local q="$crf"; [ "$twopass" = "true" ] && q="2-Pass"; [ "$q" = "null" ] && q="-"
    local audio="$abit / ${abit}"
    # 简化音频列
    audio="$abit"
    printf '%-4s %-16s %-10s %-8s %-6s %-8s %-12s %s\n' "$id" "$name" "$fps" "$res" "$color" "$q" "$audio" "$expsz"
  done
  printf '\n%s默认推荐: L4%s\n' "$C_GRN" "$C_OFF"
}

# ---------- 解析参数 ----------
INPUT=""
LEVEL=""
OUTPUT=""
YES=0
DRYRUN=0
LIST=0
TARGET=""
FORCE=0

# 第一个非选项参数=输入视频,第二个=级别(若形如 L1~L8)
parse_args() {
  while [ $# -gt 0 ]; do
    case "$1" in
      -h|--help) usage; exit 0 ;;
      -l|--list) LIST=1 ;;
      -o|--output) shift; OUTPUT="${1:-}"; [ -z "$OUTPUT" ] && { err "-o 需要一个参数"; exit 2; } ;;
      -y|--yes) YES=1 ;;
      -n|--dry-run) DRYRUN=1 ;;
      --target) shift; TARGET="${1:-}"; [ -z "$TARGET" ] && { err "--target 需要一个参数"; exit 2; } ;;
      --force) FORCE=1 ;;
      --) shift; break ;;
      -*) err "未知选项: $1"; usage; exit 2 ;;
      *)
        if [ -z "$INPUT" ]; then INPUT="$1"
        elif [ -z "$LEVEL" ]; then LEVEL="$1"
        else err "多余参数: $1"; exit 2; fi ;;
    esac
    shift
  done
}

parse_args "$@"

# ---------- --list 单独处理 ----------
if [ "$LIST" = "1" ]; then print_list; exit 0; fi

# ---------- 校验输入 ----------
if [ -z "$INPUT" ]; then err "缺少输入视频。用法: 1f6s.sh <输入视频> [级别] [选项]"; usage; exit 2; fi
if [ ! -f "$INPUT" ]; then err "输入视频不存在: $INPUT"; exit 2; fi
command -v ffmpeg  >/dev/null 2>&1 || { err "未找到 ffmpeg,请先安装。"; exit 2; }
command -v ffprobe >/dev/null 2>&1 || { err "未找到 ffprobe,请先安装(通常随 ffmpeg)。"; exit 2; }
if [ ! -f "$LEVELS_FILE" ]; then err "找不到参数源 levels.json: $LEVELS_FILE"; exit 2; fi

# 级别默认 L4,归一化为大写
LEVEL="${LEVEL:-L4}"
LEVEL="$(printf '%s' "$LEVEL" | tr '[:lower:]' '[:upper:]')"
case "$LEVEL" in
  L1|L2|L3|L4|L5|L6|L7|L8) ;;
  *) err "无效级别: $LEVEL(应为 L1~L8)"; exit 2 ;;
esac

# ---------- 取该级别参数 ----------
LJSON="$(level_json "$LEVEL")" || { err "levels.json 中找不到级别 $LEVEL"; exit 2; }
L_NAME="$(json_field "$LJSON" '.name')"
L_INTERVAL="$(json_field "$LJSON" '.interval')"
L_SCALE="$(json_field "$LJSON" '.scale')"
L_COLOR="$(json_field "$LJSON" '.color')"
L_CODEC="$(json_field "$LJSON" '.codec')"
L_CRF="$(json_field "$LJSON" '.crf')"
L_ABIT="$(json_field "$LJSON" '.audio_bitrate')"
L_ARATE="$(json_field "$LJSON" '.audio_rate')"
L_TUNE="$(json_field "$LJSON" '.tune')"
L_EXTRA="$(json_field "$LJSON" '.extra')"
L_TWOPASS="$(json_field "$LJSON" '.twopass')"
L_EXP="$(json_field "$LJSON" '.expected_size')"

# ---------- 探测源视频 ----------
SRC_DURATION="$(ffprobe -v error -show_entries format=duration -of default=nk=1:nw=1 "$INPUT" 2>/dev/null || echo 0)"
SRC_DURATION_INT="$(printf '%.0f' "${SRC_DURATION:-0}")"
SRC_W="$(ffprobe -v error -select_streams v:0 -show_entries stream=width -of default=nk=1:nw=1 "$INPUT" 2>/dev/null || echo '?')"
SRC_H="$(ffprobe -v error -select_streams v:0 -show_entries stream=height -of default=nk=1:nw=1 "$INPUT" 2>/dev/null || echo '?')"
SRC_CODEC="$(ffprobe -v error -select_streams v:0 -show_entries stream=codec_name -of default=nk=1:nw=1 "$INPUT" 2>/dev/null || echo '?')"
SRC_SIZE_BYTES="$(stat -c '%s' "$INPUT" 2>/dev/null || stat -f '%z' "$INPUT" 2>/dev/null || echo 0)"
human_size() { # <bytes>
  local b="${1:-0}"; awk -v b="$b" 'BEGIN{ if(b<1024) printf "%.0f B",b; else if(b<1048576) printf "%.1f KB",b/1024; else printf "%.2f MB",b/1048576 }'
}
SRC_SIZE_H="$(human_size "$SRC_SIZE_BYTES")"

# ---------- 输出文件名 ----------
if [ -z "$OUTPUT" ]; then
  # 默认 <basename>_1f6s.mp4,与源同目录
  SRC_DIR="$(cd "$(dirname "$INPUT")" && pwd)"
  SRC_BASE="$(basename "$INPUT")"
  SRC_NOEXT="${SRC_BASE%.*}"
  OUTPUT="$SRC_DIR/${SRC_NOEXT}_1f6s.mp4"
fi

# ---------- 平台适配: /dev/null vs NUL ----------
case "$(uname -s)" in
  MINGW*|MSYS*|CYGWIN*) NULLDEV="NUL" ;;
  *) NULLDEV="/dev/null" ;;
esac

# ---------- 构造视频滤镜链 ----------
VF="fps=${L_INTERVAL},scale=${L_SCALE}"
[ "$L_COLOR" = "gray" ] && VF="${VF},format=gray"

# ---------- 构造编码参数 ----------
ENC="-c:v ${L_CODEC} -preset slow"
if [ -n "$L_TUNE" ] && [ "$L_TUNE" != "null" ]; then ENC="${ENC} -tune ${L_TUNE}"; fi
if [ -n "$L_EXTRA" ] && [ "$L_EXTRA" != "null" ]; then
  case "$L_CODEC" in
    libx265) ENC="${ENC} -x265-params \"${L_EXTRA}\"" ;;
    *) ENC="${ENC} -x264-params \"${L_EXTRA}\"" ;;
  esac
fi

# 音频参数(全部级别统一 AAC 单声道 yuv420p)
AUDIO="-c:a aac -ac 1 -ar ${L_ARATE} -b:a ${L_ABIT}"
PIX="-pix_fmt yuv420p"

# ---------- L7 / 2-Pass 目标码率计算 ----------
PASS_BV=""
if [ "$L_TWOPASS" = "true" ]; then
  if [ -z "$TARGET" ]; then
    warn "L7 为 2-Pass 精确体积模式,未指定 --target,将使用示例码率 3k。"
    warn "如需锁定体积,请加 --target <MB>(如 --target 8)。"
    PASS_BV="3k"
  else
    # 总比特率 = 目标MB × 8192 / 秒;视频码率 = 总比特率 − 音频码率(kbps 取数字)
    local_abit_num="$(printf '%s' "$L_ABIT" | tr -dc '0-9')"
    PASS_BV="$(awk -v m="$TARGET" -v d="$SRC_DURATION_INT" -v a="$local_abit_num" 'BEGIN{
      if(d<=0){ printf "3k"; exit }
      total = m * 8192 / d
      v = total - a
      if(v<1) v=1
      printf "%.0fk", v/1
    }')"
    ok "L7 目标体积 ${TARGET}MB → 视频码率约 ${PASS_BV}(总时长 ${SRC_DURATION_INT}s,音频 ${L_ABIT})"
  fi
fi

# ---------- 组装命令字符串(用于展示与执行) ----------
quote_input() { printf '%s' "$INPUT" | sed "s/'/'\\\\''/g"; }
quote_output() { printf '%s' "$OUTPUT" | sed "s/'/'\\\\''/g"; }

build_cmd() { # build_cmd <pass: 1|2|0>
  local p="$1"
  local qin qout
  qin="'$(quote_input)'"; qout="'$(quote_output)'"
  local cmd="ffmpeg -y -i ${qin} -vf \"${VF}\" ${ENC}"
  if [ "$L_TWOPASS" = "true" ]; then
    cmd="${cmd} -b:v ${PASS_BV} -pass ${p}"
  else
    [ -n "$L_CRF" ] && [ "$L_CRF" != "null" ] && cmd="${cmd} -crf ${L_CRF}"
  fi
  if [ "$p" = "1" ]; then
    # 第一遍:只分析,丢到空设备,不输出文件、不编码音频
    cmd="${cmd} -an -f mp4 ${NULLDEV}"
  else
    cmd="${cmd} ${AUDIO} ${PIX} ${qout}"
  fi
  printf '%s' "$cmd"
}

CMD2="$(build_cmd 2)"
CMD1=""
[ "$L_TWOPASS" = "true" ] && CMD1="$(build_cmd 1)"

# ---------- 展示阶段 ----------
say ""
notice "═══════════════════════════════════════════════════════════"
notice " 1帧6秒 · ffmpeg 视频压缩  (级别 ${LEVEL} ${L_NAME})"
notice "═══════════════════════════════════════════════════════════"
say ""
printf '%s【源视频】%s\n' "$C_BOLD" "$C_OFF"
printf '  路径:     %s\n' "$INPUT"
printf '  时长:     %s 秒\n' "${SRC_DURATION:-?}"
printf '  分辨率:   %s×%s\n' "${SRC_W}" "${SRC_H}"
printf '  编码:     %s\n' "${SRC_CODEC}"
printf '  体积:     %s\n' "$SRC_SIZE_H"
say ""
printf '%s【压缩参数 · %s %s】%s\n' "$C_BOLD" "$LEVEL" "$L_NAME" "$C_OFF"
printf '  抽帧间隔: 1帧/%s秒\n' "$(printf '%s' "$L_INTERVAL" | cut -d/ -f2)"
printf '  分辨率:   %s (%s)\n' "$L_SCALE" "$([ "$L_SCALE" = "-2:480" ] && echo 480p || echo 360p)"
printf '  色彩:     %s\n' "$([ "$L_COLOR" = "gray" ] && echo 黑白 || echo 彩色)"
printf '  编码器:   %s\n' "$L_CODEC"
if [ "$L_TWOPASS" = "true" ]; then
  printf '  质量:     2-Pass(目标码率 %s)\n' "$PASS_BV"
else
  printf '  质量:     CRF %s\n' "$L_CRF"
fi
printf '  音频:     %s / %sHz / 单声道\n' "$L_ABIT" "$L_ARATE"
[ -n "$L_TUNE" ] && [ "$L_TUNE" != "null" ] && printf '  调优:     tune=%s\n' "$L_TUNE"
[ -n "$L_EXTRA" ] && [ "$L_EXTRA" != "null" ] && printf '  额外:     %s\n' "$L_EXTRA"
printf '  预期体积: %s\n' "$L_EXP"
say ""
printf '%s【输出】%s\n' "$C_BOLD" "$C_OFF"
printf '  %s\n' "$OUTPUT"
say ""
printf '%s【将执行的命令】%s\n' "$C_BOLD" "$C_OFF"
if [ -n "$CMD1" ]; then
  printf '  %s%s# 第一遍(分析)%s\n' "$C_DIM" "$C_OFF" ""
  printf '  %s\n' "$CMD1"
  printf '  %s%s# 第二遍(输出)%s\n' "$C_DIM" "$C_OFF" ""
fi
printf '  %s\n' "$CMD2"
say ""

# ---------- 输出存在性检查 ----------
if [ -e "$OUTPUT" ] && [ "$FORCE" != "1" ]; then
  err "输出文件已存在: $OUTPUT"
  err "如需覆盖,请加 --force;或用 -o 指定其它路径。"
  exit 3
fi
if [ "$OUTPUT" = "$INPUT" ]; then
  err "输出路径与源视频相同,拒绝执行(本脚本默认不覆盖原视频)。"
  err "请用 -o 指定其它输出路径。"
  exit 3
fi

# ---------- dry-run / 确认 / 执行 ----------
if [ "$DRYRUN" = "1" ]; then
  notice "(dry-run) 命令已展示,未执行。"
  exit 0
fi

if [ "$YES" != "1" ]; then
  warn "即将执行压缩$( [ -n "$CMD1" ] && printf '(%s 两遍 pass)' "$LEVEL" || printf '(%s)' "$LEVEL"),按 [y] 继续,其它键中止:"
  read -r -n1 ans
  say ""
  case "$ans" in
    y|Y) ;;
    *) warn "已中止。"; exit 130 ;;
  esac
fi

run_cmd() { # run_cmd <cmdstring>
  # 用 eval 解析转义的引号
  eval "$1"
}

notice "开始压缩…"
if [ -n "$CMD1" ]; then
  ok "[1/2] 第一遍分析…"
  run_cmd "$CMD1"
fi
if [ -n "$CMD1" ]; then
  ok "[2/2] 第二遍输出…"
else
  ok "压缩中…"
fi
run_cmd "$CMD2"

# ---------- 清理 2-Pass 残留日志 ----------
if [ "$L_TWOPASS" = "true" ]; then
  rm -f ffmpeg2pass-*.log* 2>/dev/null || true
fi

# ---------- 执行后报告 ----------
say ""
if [ -f "$OUTPUT" ]; then
  OUT_BYTES="$(stat -c '%s' "$OUTPUT" 2>/dev/null || stat -f '%z' "$OUTPUT" 2>/dev/null || echo 0)"
  OUT_H="$(human_size "$OUT_BYTES")"
  ok "压缩完成 ✓"
  printf '  输出: %s\n' "$OUTPUT"
  printf '  体积: %s → %s\n' "$SRC_SIZE_H" "$OUT_H"
  printf '  级别: %s %s\n' "$LEVEL" "$L_NAME"
  printf '  预期: %s\n' "$L_EXP"
  # 可被 ffprobe 识别?
  if ffprobe -v error -show_entries format=duration -of default=nk=1:nw=1 "$OUTPUT" >/dev/null 2>&1; then
    printf '  ffprobe 校验: %s可识别%s\n' "$C_GRN" "$C_OFF"
  else
    warn "ffprobe 校验: 输出文件无法识别,请检查。"
  fi
else
  err "未找到输出文件,压缩可能失败。请检查上方 ffmpeg 输出。"
  exit 1
fi
