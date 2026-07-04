import discord
from discord.ext import commands
import os

# ローカル環境用（.envファイルがあれば読み込む）
try:
    from dotenv import load_dotenv
    load_dotenv()
except ImportError:
    pass

# 3. 入力フォーム（モーダル）の定義
class InquiryModal(discord.ui.Modal):
    def __init__(self, target: str):
        # 選択された宛先をタイトルに表示
        super().__init__(title=f"【{target}】へのお問い合わせ")
        self.target = target

        # テキスト入力欄の設定
        self.inquiry_text = discord.ui.TextInput(
            label="お問い合わせ内容",
            style=discord.TextStyle.paragraph, # 複数行の入力に対応
            placeholder="ここに詳細な内容を入力してください...",
            required=True
        )
        self.add_item(self.inquiry_text)

    # 送信ボタンが押された時の処理
    async def on_submit(self, interaction: discord.Interaction):
        # ※実際にはここで指定のチャンネル（運営用チャンネルなど）にメッセージを送信する処理を書きます。
        # 今回はデモとして、送信した本人にだけ確認メッセージを返します。
        result_message = f"**{self.target}** へ以下のお問い合わせを送信しました。\n```\n{self.inquiry_text.value}\n```"
        await interaction.response.send_message(result_message, ephemeral=True)

# 2. ドロップダウンメニュー（セレクト）の定義
class InquirySelect(discord.ui.Select):
    def __init__(self):
        options = [
            discord.SelectOption(label="開発者", description="システムのバグや技術的な問題について", emoji="💻"),
            discord.SelectOption(label="運営", description="イベントやコミュニティ全般について", emoji="🏢"),
            discord.SelectOption(label="管理者", description="サーバーのルール違反や対人トラブルについて", emoji="👑")
        ]
        super().__init__(placeholder="お問い合わせ先を選択してください", options=options)

    # メニューが選択された時の処理
    async def callback(self, interaction: discord.Interaction):
        # 選択された項目（self.values[0]）を渡してモーダルを開く
        modal = InquiryModal(self.values[0])
        await interaction.response.send_modal(modal)

# 1. ビュー（UIコンポーネントをまとめる土台）の定義
class InquiryView(discord.ui.View):
    def __init__(self):
        super().__init__()
        self.add_item(InquirySelect())

# Bot本体のセットアップ
class MyBot(commands.Bot):
    def __init__(self):
        super().__init__(command_prefix="!", intents=discord.Intents.default())

    async def setup_hook(self):
        # スラッシュコマンドをDiscordサーバーに同期
        await self.tree.sync()

bot = MyBot()

# スラッシュコマンドの定義
@bot.tree.command(name="inquiry", description="お問い合わせ窓口を開きます")
async def inquiry(interaction: discord.Interaction):
    # ドロップダウンメニューが付いたメッセージを送信（ephemeral=Trueで実行者にしか見えないようにする）
    await interaction.response.send_message("お問い合わせ先を選んでください：", view=InquiryView(), ephemeral=True)

# Botの起動
if __name__ == "__main__":
    token = os.environ.get("DISCORD_TOKEN")
    if not token:
        print("エラー: DISCORD_TOKENが設定されていません。")
    else:
        bot.run(token)
