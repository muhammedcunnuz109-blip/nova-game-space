from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.scrollview import ScrollView
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.graphics import Color, RoundedRectangle
from kivy.metrics import dp

from jnius import autoclass


PythonActivity = autoclass(
    "org.kivy.android.PythonActivity"
)

Intent = autoclass(
    "android.content.Intent"
)

PackageManager = autoclass(
    "android.content.pm.PackageManager"
)


class NovaGameSpace(App):

    def build(self):

        root = BoxLayout(
            orientation="vertical",
            padding=[
                dp(18),
                dp(25),
                dp(18),
                dp(15)
            ],
            spacing=dp(12)
        )

        # Arka plan
        with root.canvas.before:
            Color(0.015, 0.02, 0.07, 1)

            self.background = RoundedRectangle(
                pos=root.pos,
                size=root.size
            )

        root.bind(
            pos=self.update_background,
            size=self.update_background
        )

        # Başlık
        title = Label(
            text="NOVA",
            font_size=dp(38),
            bold=True,
            color=(0.25, 0.75, 1, 1),
            size_hint_y=None,
            height=dp(55)
        )

        root.add_widget(title)

        subtitle = Label(
            text="GAME SPACE",
            font_size=dp(18),
            color=(0.65, 0.75, 0.9, 1),
            size_hint_y=None,
            height=dp(30)
        )

        root.add_widget(subtitle)

        self.status = Label(
            text="🎮 Oyunlar aranıyor...",
            font_size=dp(15),
            color=(0.7, 0.8, 0.9, 1),
            size_hint_y=None,
            height=dp(35)
        )

        root.add_widget(self.status)

        # Kaydırılabilir oyun listesi
        scroll = ScrollView()

        self.game_list = BoxLayout(
            orientation="vertical",
            spacing=dp(10),
            size_hint_y=None
        )

        self.game_list.bind(
            minimum_height=self.game_list.setter(
                "height"
            )
        )

        scroll.add_widget(self.game_list)
        root.add_widget(scroll)

        # Yenile
        refresh = Button(
            text="🔄 OYUNLARI YENİLE",
            font_size=dp(16),
            bold=True,
            size_hint_y=None,
            height=dp(55),
            background_color=(0.08, 0.35, 0.7, 1)
        )

        refresh.bind(
            on_press=lambda x:
            self.uygulamalari_getir()
        )

        root.add_widget(refresh)

        self.uygulamalari_getir()

        return root

    def update_background(self, instance, value):
        self.background.pos = instance.pos
        self.background.size = instance.size

    def uygulamalari_getir(self):

        self.game_list.clear_widgets()

        try:

            activity = PythonActivity.mActivity
            pm = activity.getPackageManager()

            intent = Intent(
                Intent.ACTION_MAIN
            )

            intent.addCategory(
                Intent.CATEGORY_LAUNCHER
            )

            apps = pm.queryIntentActivities(
                intent,
                PackageManager.MATCH_ALL
            )

            uygulamalar = []

            for info in apps:

                app_info = info.activityInfo

                package_name = str(
                    app_info.packageName
                )

                if package_name == str(
                    activity.getPackageName()
                ):
                    continue

                app_name = str(
                    app_info.loadLabel(pm)
                )

                uygulamalar.append(
                    (
                        app_name,
                        package_name
                    )
                )

            uygulamalar.sort(
                key=lambda x: x[0].lower()
            )

            for name, package_name in uygulamalar:

                self.uygulama_karti(
                    name,
                    package_name
                )

            self.status.text = (
                f"📱 {len(uygulamalar)} uygulama bulundu"
            )

        except Exception as e:

            self.status.text = (
                "❌ Uygulamalar alınamadı"
            )

            print("HATA:", e)

    def uygulama_karti(
        self,
        name,
        package_name
    ):

        card = BoxLayout(
            orientation="horizontal",
            padding=[
                dp(12),
                dp(8)
            ],
            spacing=dp(10),
            size_hint_y=None,
            height=dp(70)
        )

        with card.canvas.before:

            Color(
                0.045,
                0.07,
                0.15,
                1
            )

            card_bg = RoundedRectangle(
                pos=card.pos,
                size=card.size,
                radius=[dp(12)]
            )

        card.bind(
            pos=lambda obj, value:
            setattr(
                card_bg,
                "pos",
                value
            )
        )

        card.bind(
            size=lambda obj, value:
            setattr(
                card_bg,
                "size",
                value
            )
        )

        label = Label(
            text="🎮  " + name,
            font_size=dp(16),
            halign="left",
            valign="middle"
        )

        label.bind(
            size=lambda obj, value:
            setattr(
                obj,
                "text_size",
                value
            )
          )
