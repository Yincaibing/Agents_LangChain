from openai import OpenAI
client = OpenAI()

audio_file = open("stuiptgirl.mp3", "rb")
transcript = client.audio.transcriptions.create(
  model="whisper-1",
  file=audio_file,
  response_format="text"
)
print(transcript)

# 夜半無人 詞曲 李宗盛 仰舞奏長舟不經意地 抱著我靜看天地 仰上再無味的倚嶺上 笑說最愛你的氣味 我恨我共你試圖然而圓場的好戲 只有請你的無言從此每天飾演你 夜來別來伴我作 默念但仍默許我 將肌膚緊貼你 將身軀教育你 准許我這夜做舊角色 准我快樂地重飾演某段美麗故事主人 飾演你舊年共尋夢的戀人 再去做沒留著情侶的依人 假裝再有從前演掛的氣氛 重飾演某段美麗故事主人 飾演你舊年共尋夢的戀人 你縱使未明白仍野心一人 穿起你那無言無意當跟你折戒 Zither Harp 我恨我共你試圖然而圓場的好戲 只有請你的無言從此每天飾演你 夜來別來伴我作 默念但仍默許我 將肌膚緊貼你 將身軀教育你 准許我這夜做舊角色 准我快樂地重飾演某段美麗故事主人 飾演你舊年共尋夢的戀人 再去做沒留著情侶的依人 假裝再有從前演掛的氣氛 重飾演某段美麗故事主人 飾演你舊年共尋夢的戀人 你縱使未明白仍野心一人 穿起你那無言無意當跟你折戒 Zither Harp Zither Harp
