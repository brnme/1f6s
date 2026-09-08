#!/usr/bin/env python3
"""1帧6秒 deck 旁白配音生成：逐页 edge-tts 合成 + ffprobe 取时长 + 拼接 + 时间戳清单。
用法: gen_voiceover.py [--rate +8%] [--voice zh-CN-YunxiNeural]
产物: ~/hhhermes/1f6s/slides/voiceover/ 下
  - per-slide/slideNN.mp3   每页单独音轨
  - voiceover-full.mp3      拼接后完整配音
  - timestamps.txt          各页起始时间戳
  - timestamps.json         同上(JSON, 供后续视频制作)
"""
import argparse, json, subprocess, sys, time
from pathlib import Path

EDGE = str(Path.home() / ".venvs/tts/bin/edge-tts")
OUT = Path.home() / "hhhermes/1f6s/slides/voiceover"
PER = OUT / "per-slide"

SLIDES = [
    ("01", "一份99分钟的讲解视频，原片动辄好几个G，微信发不动，邮箱也传不上。这套倡议叫「1帧6秒」：讲解类视频，画面每6秒取一帧，就够了。"),
    ("02", "先讲这套规范的道理，再看数据，然后是怎么选级别、怎么落地。"),
    ("03", "讲解视频的价值在内容，不在画面流畅。每秒30帧里，绝大部分帧和前一帧几乎一模一样，却都在消耗你的编码器和流量。「1帧6秒」的主张是：画面只在信息变化时更新，音频完整保留。"),
    ("04", "它有明确的边界。静态为主、信息靠讲的内容，比如PPT讲解、代码演示，用它没有损失。但如果内容靠连续动作、靠表情情绪、靠精确时机，比如监控、影视、手语，请不要用这套规范。"),
    ("05", "为什么正好是6秒？人对一张静止画面的视觉记忆大概4到8秒，6秒在中间。中文正常语速一分钟150到180字，6秒正好15到18个字，刚够讲完一张幻灯片的标题。"),
    ("06", "跟5秒比，6秒一小时少120帧，体积再降将近17%。跟8秒比，6秒的音画落差小得多。还有个好处：6能整除60，看一眼时间戳的秒位，就知道现在播到第几张画面。"),
    ("07", "这张表把不同间隔摆在一起。2秒一帧，体积太大，失去压缩意义。8秒、10秒，音画错位开始明显。6秒一小时600帧，是体验和体积的平衡点。"),
    ("08", "按99分钟算，各级别体积大概是这样：彩色L1要33兆左右；转成黑白，L2降到26兆；CRF提到34，L3是20兆；再加stillimage调优，L4只要17兆半，这是默认推荐。"),
    ("09", "再往下是极限档。抽帧间隔放宽到10秒，L6只要11兆。L7用两遍编码，能精确锁定你要的体积。L8换H.265，压到7兆，但要先确认对方的播放器支持。"),
    ("10", "选级别就三个问题：发给谁、要不要彩色、对方网速如何。销售演示要保彩色，用L1；发邮箱，L4基本都能塞进附件限制；微信传手机看，L5；移动端离线缓存，L6。拿不准，就用L4。"),
    ("11", "这套倡议还有几个配套专题：八级规范的完整命令、九大场景的适配建议、绝对不能碰的红线清单、PPT抗压缩设计，还有OBS直播推流参数。"),
    ("12", "落地工具是现成的。一个Skill从主题直接生成抗压缩幻灯片，就是你眼前这种；另一个Skill一条命令把视频压成规范格式，动手前先展示命令，确认了才执行，也不会覆盖原片。"),
    ("13", "几个术语过一遍。fps=1/6，就是每6秒一帧。CRF是质量因子，数字越大体积越小、画质越低，28算视觉无损，34以上算高压缩。stillimage是静态画面专用调优。2-Pass编码两遍，用来锁死体积。"),
    ("14", "格式这边：H.265体积是H.264的一半，但老设备可能放不出来。yuv420p保证最大兼容性，导出必带。scale=-2:480是把高度缩到480，宽度自动算，还保证是偶数。"),
    ("15", "几个常见疑问。8千赫兹音频能听清吗？能，电话音质，人声频段都在，讲什么听得懂。为什么不干脆发GIF或图片？因为丢了人声，也丢了听到哪句看哪张的对应关系。"),
    ("16", "画面6秒一跳，突兀吗？讲解视频不突兀，观众本来就是看一页、听一段、再翻页。真正难受的是音画错位，这正是上限卡在6秒的原因。另外Windows和Mac命令完全通用，只有L7在Windows上要把/dev/null换成NUL。"),
    ("17", "这就是「1帧6秒」。压缩的功夫，一半在参数，一半在源头：幻灯片做得抗压缩，视频就省一大半力气。规范按CC BY 4.0开放，欢迎拿去用。"),
]

def run(cmd, **kw):
    r = subprocess.run(cmd, capture_output=True, text=True, **kw)
    if r.returncode != 0:
        raise RuntimeError(f"cmd failed: {' '.join(cmd)}\n{r.stderr[:500]}")
    return r

def dur(p):
    r = run(["ffprobe", "-v", "error", "-show_entries", "format=duration",
             "-of", "default=nk=1:nw=1", str(p)])
    return float(r.stdout.strip())

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--voice", default="zh-CN-YunxiNeural")
    ap.add_argument("--rate", default="+0%")
    ap.add_argument("--gap", type=float, default=0.6, help="页间静音秒数")
    ap.add_argument("--only", help="只重生成某一页，如 07")
    a = ap.parse_args()

    PER.mkdir(parents=True, exist_ok=True)
    todo = [s for s in SLIDES if not a.only or s[0] == a.only]
    total = len(todo)
    for i, (num, text) in enumerate(todo, 1):
        mp3 = PER / f"slide{num}.mp3"
        d = 0.0
        for attempt in (1, 2, 3):
            try:
                run([EDGE, "--voice", a.voice, f"--rate={a.rate}",
                     "--text", text, "--write-media", str(mp3)])
                d = dur(mp3)
                if d > 0.5:
                    break
            except Exception as e:
                if attempt == 3:
                    sys.exit(f"slide{num} 连续失败: {e}")
                time.sleep(2 * attempt)
        print(f"[{i}/{total}] slide{num}  {d:5.1f}s", flush=True)

    # 拼接（统一 44100 stereo 后 concat + 页间静音）
    gaps = round(dur(PER / "slide01.mp3") and 0)  # noop, keep flake quiet
    lst = OUT / "concat.txt"
    with lst.open("w") as f:
        for j, (num, _) in enumerate(SLIDES):
            if j:
                f.write(f"file 'gap.wav'\n")
            f.write(f"file 'per-slide/slide{num}.mp3'\n")
    run(["ffmpeg", "-v", "error", "-f", "lavfi",
         "-i", f"anullsrc=r=44100:cl=stereo:d={a.gap}",
         "-c:a", "libmp3lame", "-q:a", "2", str(OUT / "gap.wav"), "-y"])
    run(["ffmpeg", "-v", "error", "-f", "concat", "-safe", "0", "-i", str(lst),
         "-c:a", "libmp3lame", "-q:a", "2", str(OUT / "voiceover-full.mp3"), "-y"])

    # 时间戳
    stamps, t, rows = [], 0.0, []
    for num, text in SLIDES:
        stamps.append((num, t))
        rows.append((num, t, dur(PER / f"slide{num}.mp3")))
        t += dur(PER / f"slide{num}.mp3") + a.gap
    with (OUT / "timestamps.txt").open("w") as f:
        f.write(f"# 1帧6秒 deck 旁白时间戳  voice={a.voice} rate={a.rate} gap={a.gap}s\n")
        f.write(f"# 格式: 页码  起始  时长  (HH:MM:SS.mmm)\n")
        for num, st, d in rows:
            f.write(f"{num}  {time.strftime('%H:%M:%S', time.gmtime(st))}.{int(st*1000%1000):03d}"
                    f"  {d:5.1f}s\n")
        f.write(f"# 总时长 {time.strftime('%H:%M:%S', time.gmtime(t - a.gap))}\n")
    (OUT / "timestamps.json").write_text(json.dumps(
        {"voice": a.voice, "rate": a.rate, "gap": a.gap,
         "slides": [{"slide": n, "start": s, "duration": round(d, 3)} for n, s, d in rows],
         "total": round(t - a.gap, 3)}, ensure_ascii=False, indent=2))

    full = dur(OUT / "voiceover-full.mp3")
    print(f"\nfull: {full:.1f}s | pages: {len(SLIDES)} | out: {OUT}")

if __name__ == "__main__":
    main()
