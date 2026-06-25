"""
PRTS v16.0 - 综合集成监控终端
Kivy版本 - 可打包为安卓APK

依赖安装:
    pip install kivy kivymd

安卓打包:
    pip install buildozer
    buildozer init
    buildozer android debug

或者使用云打包服务如 Buildozer Web
"""

import os
import json
import datetime
import threading
import calendar
import random
from kivy.lang import Builder
from kivy.core.window import Window
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.scrollview import ScrollView
from kivy.uix.popup import Popup
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.widget import Widget
from kivy.properties import StringProperty, ListProperty, NumericProperty
from kivy.graphics import Color, Rectangle, RoundedRectangle, Line
from kivy.clock import Clock
from kivy.utils import get_color_from_hex
from kivy.metrics import dp

# ============================================================
# 颜色配置
# ============================================================
COLOR_PALETTE = {
    "bg_main": "#F4F6F9",
    "bg_card": "#FFFFFF",
    "text_main": "#1A1A1A",
    "text_sub": "#666666",
    "accent": "#00BAFF",
    "danger": "#FF4D4F",
    "terminal": "#121212"
}

# ============================================================
# 数据存储路径
# ============================================================
DATA_DIR = "prts_data"
for path in [DATA_DIR]:
    if not os.path.exists(path):
        os.makedirs(path)

CONFIG_FILE = os.path.join(DATA_DIR, "app_config.json")
EXPENSE_FILE = os.path.join(DATA_DIR, "expenses.json")
STORAGE_FILE = os.path.join(DATA_DIR, "storage.json")
TODO_FILE = os.path.join(DATA_DIR, "todos.json")
DIARY_FILE = os.path.join(DATA_DIR, "diaries.json")
LOG_FILE = os.path.join(DATA_DIR, "logs.json")

# ============================================================
# Kivy KV 布局定义
# ============================================================
KV_CODE = """
#:set accent_color get_color_from_hex(COLOR_PALETTE["accent"])
#:set bg_card get_color_from_hex(COLOR_PALETTE["bg_card"])
#:set text_main get_color_from_hex(COLOR_PALETTE["text_main"])
#:set text_sub get_color_from_hex(COLOR_PALETTE["text_sub"])
#:set danger get_color_from_hex(COLOR_PALETTE["danger"])
#:set bg_main get_color_from_hex(COLOR_PALETTE["bg_main"])

<CustomButton@Button>:
    background_color: (0,0,0,0)
    background_normal: ''
    bold: True

<Card@BoxLayout>:
    orientation: 'vertical'
    padding: 15
    spacing: 10
    canvas.before:
        Color:
            rgba: bg_card
        RoundedRectangle:
            size: self.size
            pos: self.pos
            radius: [20,]

<MainScreen>:
    name: 'main'
    BoxLayout:
        orientation: 'vertical'
        padding: 15
        spacing: 10
        
        # 顶部状态条
        Widget:
            size_hint_y: None
            height: 4
            canvas.before:
                Color:
                    rgba: accent_color
                Rectangle:
                    size: self.size
                    pos: self.pos
        
        # 左侧面板
        Card:
            size_hint_y: None
            height: 280
            BoxLayout:
                orientation: 'vertical'
                spacing: 5
                Label:
                    text: "系统运行状态"
                    font_size: 16
                    bold: True
                    color: accent_color
                    size_hint_y: None
                    height: 30
                
                Label:
                    id: lbl_time
                    text: "00:00:00"
                    font_size: 48
                    bold: True
                    color: text_main
                
                Label:
                    id: lbl_date
                    text: "----/--/--"
                    font_size: 14
                    color: text_sub
                    size_hint_y: None
                    height: 25
                
                Widget:
                    size_hint_y: None
                    height: 15
                
                # 进度条部分
                Label:
                    text: "生命周期分析"
                    font_size: 12
                    color: text_sub
                    size_hint_y: None
                    height: 20
                
                ProgressBar:
                    id: progress_bar
                    max: 100
                    value: 0
                    height: 12
                    background_color: get_color_from_hex("#E8E8E8")
                    color: accent_color
                
                Label:
                    id: lbl_percent
                    text: "0%"
                    font_size: 28
                    bold: True
                    color: accent_color
                    size_hint_y: None
                    height: 35
                
                Label:
                    id: lbl_cycle_info
                    text: "同步中..."
                    font_size: 11
                    color: text_sub
                    size_hint_y: None
                    height: 20
                
                Widget:
                    size_hint_y: None
                    height: 10
                
                # 天气信息
                BoxLayout:
                    orientation: 'vertical'
                    size_hint_y: None
                    height: 50
                    padding: 10
                    canvas.before:
                        Color:
                            rgba: get_color_from_hex("#F8F9FA")
                        RoundedRectangle:
                            size: self.size
                            pos: self.pos
                            radius: [12,]
                    
                    Label:
                        id: weather_city
                        text: "正在连接气象卫星..."
                        font_size: 13
                        bold: True
                        color: text_main
                        text_size: self.size
                        halign: 'left'
                    
                    Label:
                        id: weather_desc
                        text: "等待同步..."
                        font_size: 12
                        color: text_sub
                        text_size: self.size
                        halign: 'left'
        
        # 中间圆形装饰
        BoxLayout:
            size_hint_y: None
            height: 180
            padding: 10
            Card:
                size_hint: None, None
                size: 160, 160
                pos_hint: {'center_x': 0.5}
                padding: 0
                BoxLayout:
                    alignment: 'center'
                    Label:
                        text: "🌱"
                        font_size: 70
                        size: 120, 120
                        canvas.before:
                            Color:
                                rgba: accent_color
                            Line:
                                circle: self.center_x, self.center_y, 60, 0, 360
                                width: 4
                
                Button:
                    id: btn_action
                    text: "同步数据至 PRTS 核心"
                    size_hint: None, None
                    size: 220, 50
                    pos_hint: {'center_x': 0.5, 'y': 0}
                    background_color: accent_color
                    color: [1,1,1,1]
                    bold: True
                    border_radius: [25,]
                    on_release: root.on_sync_click()
        
        # 工具栏
        BoxLayout:
            size_hint_y: None
            height: 50
            spacing: 8
            padding: 5
            canvas.before:
                Color:
                    rgba: bg_card
                RoundedRectangle:
                    size: self.size
                    pos: self.pos
                    radius: [25,]
            
            Button:
                text: "🖼️ 背景"
                background_color: get_color_from_hex("#4A4A4A")
                on_release: root.show_bg_picker()
            
            Button:
                text: "🎨 主题"
                background_color: get_color_from_hex("#4A4A4A")
                on_release: root.show_theme_picker()
            
            Button:
                text: "💰 预算"
                background_color: get_color_from_hex("#4A4A4A")
                on_release: root.show_budget_input()
            
            Button:
                text: "⚠️ 删档"
                background_color: danger
                on_release: root.show_reset_confirm()
        
        # 选项卡面板
        BoxLayout:
            orientation: 'vertical'
            canvas.before:
                Color:
                    rgba: bg_card
                RoundedRectangle:
                    size: self.size
                    pos: self.pos
                    radius: [20,]
            
            # 选项卡标题
            BoxLayout:
                size_hint_y: None
                height: 45
                padding: 5
                spacing: 5
                canvas.before:
                    Color:
                        rgba: get_color_from_hex("#F8F8F8")
                    Rectangle:
                        size: self.size
                        pos: self.pos
                
                Button:
                    id: tab_finance_btn
                    text: "💰 资产"
                    background_color: accent_color if root.current_tab == 'finance' else get_color_from_hex("#DDDDDD")
                    color: accent_color if root.current_tab == 'finance' else text_sub
                    on_release: root.switch_tab('finance')
                
                Button:
                    id: tab_storage_btn
                    text: "📦 存储"
                    background_color: accent_color if root.current_tab == 'storage' else get_color_from_hex("#DDDDDD")
                    color: accent_color if root.current_tab == 'storage' else text_sub
                    on_release: root.switch_tab('storage')
                
                Button:
                    id: tab_todo_btn
                    text: "📋 待办"
                    background_color: accent_color if root.current_tab == 'todo' else get_color_from_hex("#DDDDDD")
                    color: accent_color if root.current_tab == 'todo' else text_sub
                    on_release: root.switch_tab('todo')
                
                Button:
                    id: tab_diary_btn
                    text: "📝 日志"
                    background_color: accent_color if root.current_tab == 'diary' else get_color_from_hex("#DDDDDD")
                    color: accent_color if root.current_tab == 'diary' else text_sub
                    on_release: root.switch_tab('diary')
                
                Button:
                    id: tab_console_btn
                    text: "💻 控制台"
                    background_color: accent_color if root.current_tab == 'console' else get_color_from_hex("#DDDDDD")
                    color: accent_color if root.current_tab == 'console' else text_sub
                    on_release: root.switch_tab('console')
            
            # 选项卡内容区域
            ScrollView:
                id: tab_container
                size_hint_y: 1
        
        Widget:
            size_hint_y: None
            height: 10
"""

# ============================================================
# 主应用类
# ============================================================
class PRTSApp:
    """PRTS - 赛博农场主应用类"""
    
    def __init__(self):
        # 运行时数据
        self.config = {
            "theme_color": COLOR_PALETTE["accent"],
            "monthly_budget": 3000.0,
            "bg_gradient_start": "#667eea",
            "bg_gradient_end": "#764ba2"
        }
        
        self.expenses = []
        self.storage_items = []
        self.todo_items = []
        self.diaries = []
        self.logs = []
        
        # 编辑状态
        self.editing_fin_idx = -1
        self.editing_store_idx = -1
        self.editing_todo_idx = -1
        
        # 加载数据
        self.load_all_data()
        
        # 初始化Kivy应用
        from kivy.app import App
        from kivy.core.text import LabelBase
        from kivy.graphics import Color as GColor
        
        # 注册中文字体（使用系统默认）
        
    def load_all_data(self):
        """加载所有数据文件"""
        self.config = self.load_json(CONFIG_FILE, self.config)
        self.expenses = self.load_json(EXPENSE_FILE, [])
        self.storage_items = self.load_json(STORAGE_FILE, [])
        self.todo_items = self.load_json(TODO_FILE, [])
        self.diaries = self.load_json(DIARY_FILE, [])
        self.logs = self.load_json(LOG_FILE, [])
    
    def save_all_data(self):
        """保存所有数据文件"""
        self.save_json(CONFIG_FILE, self.config)
        self.save_json(EXPENSE_FILE, self.expenses)
        self.save_json(STORAGE_FILE, self.storage_items)
        self.save_json(TODO_FILE, self.todo_items)
        self.save_json(DIARY_FILE, self.diaries)
        self.save_json(LOG_FILE, self.logs)
    
    def load_json(self, filepath, default):
        """加载JSON文件"""
        try:
            if os.path.exists(filepath):
                with open(filepath, 'r', encoding='utf-8') as f:
                    return json.load(f)
        except Exception as e:
            print(f"加载文件失败 {filepath}: {e}")
        return default
    
    def save_json(self, filepath, data):
        """保存JSON文件"""
        try:
            with open(filepath, 'w', encoding='utf-8') as f:
                json.dump(data, f, ensure_ascii=False, indent=2)
        except Exception as e:
            print(f"保存文件失败 {filepath}: {e}")
    
    def add_log(self, message):
        """添加日志"""
        timestamp = datetime.datetime.now().strftime("%H:%M:%S")
        self.logs.insert(0, f"[{timestamp}] {message}")
        if len(self.logs) > 100:
            self.logs = self.logs[:100]
        self.save_json(LOG_FILE, self.logs)
    
    def get_cycle_range(self):
        """获取当前周期（月份）的开始和结束日期"""
        now = datetime.datetime.now()
        start = datetime.datetime(now.year, now.month, 1)
        if now.month == 12:
            end = datetime.datetime(now.year + 1, 1, 1) - datetime.timedelta(seconds=1)
        else:
            end = datetime.datetime(now.year, now.month + 1, 1) - datetime.timedelta(seconds=1)
        return start, end
    
    def calculate_remaining_budget(self):
        """计算剩余预算"""
        start, end = self.get_cycle_range()
        spent = 0.0
        for item in self.expenses:
            try:
                it = datetime.datetime.strptime(item["date"], "%Y-%m-%d %H:%M:%S")
                if start <= it <= end:
                    spent += item["amount"]
            except:
                pass
        return self.config.get("monthly_budget", 3000.0) - spent


# ============================================================
# Kivy 应用入口（简化版本，用于测试）
# ============================================================
Builder.load_string(KV_CODE)


class MainScreen(Screen):
    """主界面"""
    current_tab = StringProperty('finance')
    
    def __init__(self, app, **kwargs):
        super().__init__(**kwargs)
        self.app = app
        self.current_tab = 'finance'
        
        # 启动定时更新
        Clock.schedule_interval(self.update_time, 1)
        Clock.schedule_interval(self.update_cycle_info, 60)
        
        # 初始加载
        self.update_time()
        self.update_cycle_info()
        self.switch_tab('finance')
        self.app.add_log('神经链路已建立。终端校准完成。')
    
    def update_time(self, *args):
        """更新时间显示"""
        now = datetime.datetime.now()
        self.ids.lbl_time.text = now.strftime("%H:%M:%S")
        self.ids.lbl_date.text = now.strftime("%Y / %m / %d")
    
    def update_cycle_info(self, *args):
        """更新周期信息"""
        now = datetime.datetime.now()
        day = now.day
        days_in_month = calendar.monthrange(now.year, now.month)[1]
        percent = int((day / days_in_month) * 100)
        remaining = days_in_month - day
        
        self.ids.progress_bar.value = percent
        self.ids.lbl_percent.text = f"{percent}%"
        self.ids.lbl_cycle_info.text = f"剩余 {remaining} 天完成本月周期"
        
        # 更新天气（模拟）
        cities = ['罗德岛', '龙门', '哥伦比亚', '维多利亚']
        descs = ['晴朗', '多云', '微风', '晴转多云']
        self.ids.weather_city.text = '📍 ' + random.choice(cities)
        self.ids.weather_desc.text = f"{random.choice(descs)} {random.randint(15, 30)}°C"
    
    def switch_tab(self, tab_name):
        """切换选项卡"""
        self.current_tab = tab_name
        
        # 更新按钮样式
        btn_map = {
            'finance': self.ids.tab_finance_btn,
            'storage': self.ids.tab_storage_btn,
            'todo': self.ids.tab_todo_btn,
            'diary': self.ids.tab_diary_btn,
            'console': self.ids.tab_console_btn
        }
        
        for name, btn in btn_map.items():
            if name == tab_name:
                btn.background_color = get_color_from_hex(self.app.config.get("theme_color", "#00BAFF"))
                btn.color = [1, 1, 1, 1]
            else:
                btn.background_color = get_color_from_hex("#DDDDDD")
                btn.color = get_color_from_hex("#666666")
        
        # 加载对应内容
        self.load_tab_content(tab_name)
    
    def load_tab_content(self, tab_name):
        """加载选项卡内容"""
        container = self.ids.tab_container
        
        # 清除现有内容
        container.clear_widgets()
        
        if tab_name == 'finance':
            self.load_finance_tab(container)
        elif tab_name == 'storage':
            self.load_storage_tab(container)
        elif tab_name == 'todo':
            self.load_todo_tab(container)
        elif tab_name == 'diary':
            self.load_diary_tab(container)
        elif tab_name == 'console':
            self.load_console_tab(container)
    
    def load_finance_tab(self, container):
        """加载资产选项卡"""
        from kivy.uix.boxlayout import BoxLayout
        from kivy.uix.label import Label
        
        layout = BoxLayout(orientation='vertical', padding=15, spacing=10)
        
        # 金额显示卡片
        remaining = self.app.calculate_remaining_budget()
        remaining_color = "#E74C3C" if remaining < 300 else "#2ECC71"
        
        amount_card = BoxLayout(orientation='vertical', padding=15, size_hint_y=None, height=100)
        amount_card.canvas.before.append(Color(rgba=get_color_from_hex("#F8FAFC")))
        amount_card.canvas.before.append(RoundedRectangle(size=amount_card.size, pos=amount_card.pos, radius=[15,]))
        
        lbl = Label(text="本期预计剩余金额", font_size=12, color=get_color_from_hex("#666666"), size_hint_y=None, height=20)
        amount_card.add_widget(lbl)
        
        money_lbl = Label(text=f"¥ {remaining:.2f}", font_size=32, bold=True, 
                         color=get_color_from_hex(remaining_color))
        amount_card.add_widget(money_lbl)
        layout.add_widget(amount_card)
        
        # 输入区域
        input_row = BoxLayout(size_hint_y=None, height=45, spacing=10)
        
        self.fin_amount_input = TextInput(hint_text="金额", multiline=False, 
                                          size_hint_x=0.25, font_size=14)
        self.fin_note_input = TextInput(hint_text="支出备注...", multiline=False,
                                        size_hint_x=0.75, font_size=14)
        input_row.add_widget(self.fin_amount_input)
        input_row.add_widget(self.fin_note_input)
        layout.add_widget(input_row)
        
        add_btn = Button(text="录入流水记录", size_hint_y=None, height=45,
                        background_color=get_color_from_hex(self.app.config.get("theme_color", "#00BAFF")),
                        color=[1,1,1,1], bold=True, border_radius=[12,])
        add_btn.bind(on_release=lambda x: self.add_expense())
        layout.add_widget(add_btn)
        
        # 流水列表
        scroll = ScrollView(size_hint_y=1)
        list_layout = BoxLayout(orientation='vertical', size_hint_y=None, spacing=5)
        list_layout.bind(minimum_height=list_layout.setter('height'))
        
        for i, item in enumerate(self.app.expenses):
            item_card = BoxLayout(orientation='horizontal', size_hint_y=None, height=50, padding=10)
            item_card.canvas.before.append(Color(rgba=get_color_from_hex("#FFFFFF")))
            item_card.canvas.before.append(RoundedRectangle(size=item_card.size, pos=item_card.pos, radius=[10,]))
            
            icon_lbl = Label(text="💸", font_size=18, size_hint_x=None, width=40)
            info_lbl = Label(text=f"¥{item['amount']:.2f} - {item['note']}\n{item['date']}", 
                            font_size=11, color=get_color_from_hex("#1A1A1A"),
                            text_size=(200, None), size_hint_x=0.7, halign='left', valign='middle')
            del_btn = Button(text="×", font_size=18, size_hint_x=None, width=35,
                           background_color=[0,0,0,0], color=get_color_from_hex("#FF4D4F"))
            del_btn.bind(on_release=lambda x, idx=i: self.delete_expense(idx))
            
            item_card.add_widget(icon_lbl)
            item_card.add_widget(info_lbl)
            item_card.add_widget(del_btn)
            list_layout.add_widget(item_card)
        
        scroll.add_widget(list_layout)
        layout.add_widget(scroll)
        container.add_widget(layout)
    
    def add_expense(self):
        """添加支出记录"""
        try:
            amt = float(self.fin_amount_input.text)
            note = self.fin_note_input.text.strip() or "未分类物资"
            d = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            
            self.app.expenses.insert(0, {"date": d, "amount": amt, "note": note})
            self.app.add_log(f"支出流水录入：¥{amt} ({note})")
            self.app.save_all_data()
            
            self.fin_amount_input.text = ''
            self.fin_note_input.text = ''
            self.switch_tab('finance')
        except ValueError:
            print("请输入有效的数字金额")
    
    def delete_expense(self, idx):
        """删除支出记录"""
        self.app.expenses.pop(idx)
        self.app.save_all_data()
        self.switch_tab('finance')
    
    def load_storage_tab(self, container):
        """加载存储选项卡"""
        from kivy.uix.boxlayout import BoxLayout
        from kivy.uix.label import Label
        
        layout = BoxLayout(orientation='vertical', padding=15, spacing=10)
        
        # 输入区域
        row1 = BoxLayout(size_hint_y=None, height=40, spacing=10)
        self.store_type_input = TextInput(hint_text="类型", multiline=False, size_hint_x=0.25, font_size=13)
        self.store_name_input = TextInput(hint_text="物品名称", multiline=False, size_hint_x=0.75, font_size=13)
        row1.add_widget(self.store_type_input)
        row1.add_widget(self.store_name_input)
        layout.add_widget(row1)
        
        row2 = BoxLayout(size_hint_y=None, height=40, spacing=10)
        self.store_status_input = TextInput(hint_text="状态", multiline=False, size_hint_x=0.25, font_size=13)
        add_btn = Button(text="存入仓库", background_color=get_color_from_hex(self.app.config.get("theme_color", "#00BAFF")),
                        color=[1,1,1,1], bold=True, border_radius=[12,])
        add_btn.bind(on_release=lambda x: self.add_storage_item())
        row2.add_widget(self.store_status_input)
        row2.add_widget(add_btn)
        layout.add_widget(row2)
        
        # 列表
        scroll = ScrollView(size_hint_y=1)
        list_layout = BoxLayout(orientation='vertical', size_hint_y=None, spacing=5)
        list_layout.bind(minimum_height=list_layout.setter('height'))
        
        for i, item in enumerate(self.app.storage_items):
            item_card = BoxLayout(orientation='horizontal', size_hint_y=None, height=50, padding=10)
            item_card.canvas.before.append(Color(rgba=get_color_from_hex("#FFFFFF")))
            item_card.canvas.before.append(RoundedRectangle(size=item_card.size, pos=item_card.pos, radius=[10,]))
            
            icon_lbl = Label(text="📦", font_size=18, size_hint_x=None, width=40)
            info_lbl = Label(text=f"{item['type']} - {item['name']}\n[{item.get('status', '在库')}]",
                            font_size=11, color=get_color_from_hex("#1A1A1A"), size_hint_x=0.7)
            del_btn = Button(text="×", font_size=18, size_hint_x=None, width=35,
                           background_color=[0,0,0,0], color=get_color_from_hex("#FF4D4F"))
            del_btn.bind(on_release=lambda x, idx=i: self.delete_storage(idx))
            
            item_card.add_widget(icon_lbl)
            item_card.add_widget(info_lbl)
            item_card.add_widget(del_btn)
            list_layout.add_widget(item_card)
        
        scroll.add_widget(list_layout)
        layout.add_widget(scroll)
        container.add_widget(layout)
    
    def add_storage_item(self):
        """添加存储物品"""
        t = self.store_type_input.text.strip()
        n = self.store_name_input.text.strip()
        s = self.store_status_input.text.strip() or "在库"
        
        if not (t and n):
            return
        
        self.app.storage_items.append({"type": t, "name": n, "status": s})
        self.app.add_log(f"仓库变动：存入 {t}-{n}")
        self.app.save_all_data()
        
        self.store_type_input.text = ''
        self.store_name_input.text = ''
        self.store_status_input.text = ''
        self.switch_tab('storage')
    
    def delete_storage(self, idx):
        """删除存储物品"""
        self.app.storage_items.pop(idx)
        self.app.save_all_data()
        self.switch_tab('storage')
    
    def load_todo_tab(self, container):
        """加载待办选项卡"""
        from kivy.uix.boxlayout import BoxLayout
        from kivy.uix.label import Label
        
        layout = BoxLayout(orientation='vertical', padding=15, spacing=10)
        
        # 输入区域
        row1 = BoxLayout(size_hint_y=None, height=40)
        self.todo_content_input = TextInput(hint_text="指令内容...", multiline=False, font_size=13)
        row1.add_widget(self.todo_content_input)
        layout.add_widget(row1)
        
        row2 = BoxLayout(size_hint_y=None, height=40, spacing=10)
        self.todo_reminder_input = TextInput(hint_text="提醒 (MM-DD HH:MM)", multiline=False, size_hint_x=0.65, font_size=13)
        add_btn = Button(text="下达指令", size_hint_x=0.35,
                        background_color=get_color_from_hex(self.app.config.get("theme_color", "#00BAFF")),
                        color=[1,1,1,1], bold=True, border_radius=[12,])
        add_btn.bind(on_release=lambda x: self.add_todo())
        row2.add_widget(self.todo_reminder_input)
        row2.add_widget(add_btn)
        layout.add_widget(row2)
        
        # 列表
        scroll = ScrollView(size_hint_y=1)
        list_layout = BoxLayout(orientation='vertical', size_hint_y=None, spacing=5)
        list_layout.bind(minimum_height=list_layout.setter('height'))
        
        for i, item in enumerate(self.app.todo_items):
            item_card = BoxLayout(orientation='horizontal', size_hint_y=None, height=50, padding=10)
            item_card.canvas.before.append(Color(rgba=get_color_from_hex("#FFFFFF")))
            item_card.canvas.before.append(RoundedRectangle(size=item_card.size, pos=item_card.pos, radius=[10,]))
            
            check_text = "✅" if item.get('done') else "○"
            check_btn = Button(text=check_text, font_size=16, size_hint_x=None, width=40,
                             background_color=[0,0,0,0], color=get_color_from_hex("#333333"))
            check_btn.bind(on_release=lambda x, idx=i: self.toggle_todo(idx))
            
            reminder_text = f"\n🔔 {item['reminder']}" if item.get('reminder') else ""
            info_lbl = Label(text=f"{item['content']}{reminder_text}",
                            font_size=12, color=get_color_from_hex("#AAAAAA" if item.get('done') else "#1A1A1A"),
                            size_hint_x=0.6, halign='left', valign='middle')
            
            del_btn = Button(text="×", font_size=18, size_hint_x=None, width=35,
                           background_color=[0,0,0,0], color=get_color_from_hex("#FF4D4F"))
            del_btn.bind(on_release=lambda x, idx=i: self.delete_todo(idx))
            
            item_card.add_widget(check_btn)
            item_card.add_widget(info_lbl)
            item_card.add_widget(del_btn)
            list_layout.add_widget(item_card)
        
        scroll.add_widget(list_layout)
        layout.add_widget(scroll)
        container.add_widget(layout)
    
    def add_todo(self):
        """添加待办"""
        c = self.todo_content_input.text.strip()
        r = self.todo_reminder_input.text.strip()
        
        if not c:
            return
        
        self.app.todo_items.insert(0, {"content": c, "reminder": r, "done": False})
        self.app.add_log(f"待办指令：{c}")
        self.app.save_all_data()
        
        self.todo_content_input.text = ''
        self.todo_reminder_input.text = ''
        self.switch_tab('todo')
    
    def toggle_todo(self, idx):
        """切换待办状态"""
        self.app.todo_items[idx]['done'] = not self.app.todo_items[idx].get('done', False)
        self.app.save_all_data()
        self.switch_tab('todo')
    
    def delete_todo(self, idx):
        """删除待办"""
        self.app.todo_items.pop(idx)
        self.app.save_all_data()
        self.switch_tab('todo')
    
    def load_diary_tab(self, container):
        """加载日记选项卡"""
        from kivy.uix.boxlayout import BoxLayout
        from kivy.uix.label import Label
        
        layout = BoxLayout(orientation='vertical', padding=15, spacing=10)
        
        # 输入区域
        row1 = BoxLayout(size_hint_y=None, height=80)
        self.diary_input = TextInput(hint_text="记录工作内容...", multiline=True, font_size=13)
        row1.add_widget(self.diary_input)
        layout.add_widget(row1)
        
        add_btn = Button(text="记录日志", size_hint_y=None, height=45,
                        background_color=get_color_from_hex(self.app.config.get("theme_color", "#00BAFF")),
                        color=[1,1,1,1], bold=True, border_radius=[12,])
        add_btn.bind(on_release=lambda x: self.add_diary())
        layout.add_widget(add_btn)
        
        # 列表
        scroll = ScrollView(size_hint_y=1)
        list_layout = BoxLayout(orientation='vertical', size_hint_y=None, spacing=5)
        list_layout.bind(minimum_height=list_layout.setter('height'))
        
        for item in self.app.diaries:
            item_card = BoxLayout(orientation='vertical', size_hint_y=None, height=80, padding=10)
            item_card.canvas.before.append(Color(rgba=get_color_from_hex("#FFFFFF")))
            item_card.canvas.before.append(RoundedRectangle(size=item_card.size, pos=item_card.pos, radius=[12,]))
            
            date_lbl = Label(text=item['date'], font_size=10, color=get_color_from_hex("#999999"),
                           size_hint_y=None, height=20, halign='left')
            content_lbl = Label(text=item['content'], font_size=12, color=get_color_from_hex("#1A1A1A"),
                              text_size=(280, None), halign='left', valign='top')
            
            item_card.add_widget(date_lbl)
            item_card.add_widget(content_lbl)
            list_layout.add_widget(item_card)
        
        scroll.add_widget(list_layout)
        layout.add_widget(scroll)
        container.add_widget(layout)
    
    def add_diary(self):
        """添加日记"""
        c = self.diary_input.text.strip()
        if not c:
            return
        
        self.app.diaries.insert(0, {"date": datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"), "content": c})
        self.app.add_log("工作日志已记录")
        self.app.save_all_data()
        
        self.diary_input.text = ''
        self.switch_tab('diary')
    
    def load_console_tab(self, container):
        """加载控制台选项卡"""
        from kivy.uix.boxlayout import BoxLayout
        from kivy.uix.label import Label
        
        layout = BoxLayout(orientation='vertical', padding=10)
        
        console = BoxLayout(orientation='vertical', padding=10)
        console.canvas.before.append(Color(rgba=get_color_from_hex("#121212")))
        console.canvas.before.append(RoundedRectangle(size=console.size, pos=console.pos, radius=[12,]))
        
        log_text = "\n".join(self.app.logs) if self.app.logs else "[ SYSTEM ] 控制台已就绪"
        log_lbl = Label(text=log_text, font_size=11, color=get_color_from_hex("#00FF41"),
                       text_size=(320, None), halign='left', valign='top')
        
        console.add_widget(log_lbl)
        layout.add_widget(console)
        container.add_widget(layout)
    
    def on_sync_click(self):
        """同步按钮点击"""
        self.ids.btn_action.text = "同步中..."
        self.ids.btn_action.disabled = True
        self.app.add_log("数据同步中...")
        
        Clock.schedule_once(lambda dt: self.on_sync_complete(), 1.5)
    
    def on_sync_complete(self):
        """同步完成"""
        self.ids.btn_action.text = "同步完成 ✓"
        self.app.add_log("数据同步完成")
        
        Clock.schedule_once(lambda dt: self.reset_sync_button(), 1.5)
    
    def reset_sync_button(self):
        """重置同步按钮"""
        self.ids.btn_action.text = "同步数据至 PRTS 核心"
        self.ids.btn_action.disabled = False
    
    def show_bg_picker(self):
        """显示背景选择器"""
        from kivy.uix.boxlayout import BoxLayout
        from kivy.uix.popup import Popup
        
        content = BoxLayout(orientation='vertical', padding=20, spacing=15, size_hint_y=None)
        content.height = 250
        
        lbl = Label(text="选择背景渐变", font_size=16, bold=True, size_hint_y=None, height=30)
        content.add_widget(lbl)
        
        gradients = [
            ("#667eea", "#764ba2", "紫色渐变"),
            ("#11998e", "#38ef7d", "绿色渐变"),
            ("#fc4a1a", "#f7b733", "橙红渐变"),
            ("#0f0c29", "#302b63", "深紫渐变")
        ]
        
        for start, end, name in gradients:
            btn = Button(text=name, size_hint_y=None, height=40, background_color=get_color_from_hex(start),
                        color=[1,1,1,1], border_radius=[12,])
            btn.bind(on_release=lambda x, s=start, e=end: self.set_bg_gradient(s, e))
            content.add_widget(btn)
        
        close_btn = Button(text="关闭", size_hint_y=None, height=40, background_color=get_color_from_hex("#DDDDDD"),
                          color=get_color_from_hex("#333333"))
        close_btn.bind(on_release=lambda x: popup.dismiss())
        content.add_widget(close_btn)
        
        popup = Popup(title='', content=content, size_hint=(0.8, None), height=280,
                    background_color=[1,1,1,1], separator_height=0)
        popup.open()
    
    def set_bg_gradient(self, start, end):
        """设置背景渐变"""
        self.app.config["bg_gradient_start"] = start
        self.app.config["bg_gradient_end"] = end
        self.app.save_all_data()
        # 注意：Kivy中设置整体背景比较复杂，这里只保存配置
    
    def show_theme_picker(self):
        """显示主题选择器"""
        from kivy.uix.boxlayout import BoxLayout
        from kivy.uix.popup import Popup
        
        content = BoxLayout(orientation='vertical', padding=20, spacing=15, size_hint_y=None)
        content.height = 300
        
        lbl = Label(text="选择主题颜色", font_size=16, bold=True, size_hint_y=None, height=30)
        content.add_widget(lbl)
        
        colors = ["#00BAFF", "#667eea", "#E74C3C", "#2ECC71", "#9B59B6", "#F39C12"]
        names = ["蓝色", "紫色", "红色", "绿色", "紫色2", "橙色"]
        
        color_grid = BoxLayout(orientation='horizontal', size_hint_y=None, height=100, spacing=10)
        for i in range(0, 6, 2):
            col = BoxLayout(orientation='vertical', spacing=10)
            for j in range(2):
                if i + j < len(colors):
                    btn = Button(background_color=get_color_from_hex(colors[i+j]), size_hint_y=None, height=40,
                                border_radius=[20,])
                    btn.bind(on_release=lambda x, c=colors[i+j]: self.set_theme_color(c))
                    col.add_widget(btn)
            color_grid.add_widget(col)
        
        content.add_widget(color_grid)
        
        close_btn = Button(text="关闭", size_hint_y=None, height=40, background_color=get_color_from_hex("#DDDDDD"),
                          color=get_color_from_hex("#333333"))
        close_btn.bind(on_release=lambda x: popup.dismiss())
        content.add_widget(close_btn)
        
        popup = Popup(title='', content=content, size_hint=(0.8, None), height=320,
                    background_color=[1,1,1,1], separator_height=0)
        popup.open()
    
    def set_theme_color(self, color):
        """设置主题颜色"""
        self.app.config["theme_color"] = color
        self.app.save_all_data()
        self.switch_tab(self.current_tab)  # 刷新界面
    
    def show_budget_input(self):
        """显示预算输入"""
        from kivy.uix.boxlayout import BoxLayout
        from kivy.uix.popup import Popup
        
        content = BoxLayout(orientation='vertical', padding=20, spacing=15)
        
        lbl = Label(text="设置月度预算", font_size=16, bold=True, size_hint_y=None, height=30)
        content.add_widget(lbl)
        
        self.budget_input = TextInput(text=str(self.app.config.get("monthly_budget", 3000)),
                                      multiline=False, font_size=18, halign='center',
                                      size_hint_y=None, height=50)
        content.add_widget(self.budget_input)
        
        btn_row = BoxLayout(size_hint_y=None, height=40, spacing=10)
        save_btn = Button(text="保存", background_color=get_color_from_hex(self.app.config.get("theme_color", "#00BAFF")),
                         color=[1,1,1,1], bold=True, border_radius=[12,])
        save_btn.bind(on_release=lambda x: self.save_budget())
        close_btn = Button(text="取消", background_color=get_color_from_hex("#DDDDDD"),
                          color=get_color_from_hex("#333333"), border_radius=[12,])
        close_btn.bind(on_release=lambda x: popup.dismiss())
        btn_row.add_widget(save_btn)
        btn_row.add_widget(close_btn)
        content.add_widget(btn_row)
        
        popup = Popup(title='', content=content, size_hint=(0.8, None), height=220,
                    background_color=[1,1,1,1], separator_height=0)
        popup.open()
    
    def save_budget(self):
        """保存预算"""
        try:
            budget = float(self.budget_input.text)
            self.app.config["monthly_budget"] = budget
            self.app.save_all_data()
            self.app.add_log(f"月度预算已更新：¥{budget}")
            self.switch_tab(self.current_tab)
        except ValueError:
            pass
    
    def show_reset_confirm(self):
        """显示重置确认"""
        from kivy.uix.boxlayout import BoxLayout
        from kivy.uix.popup import Popup
        
        content = BoxLayout(orientation='vertical', padding=20, spacing=15)
        
        lbl = Label(text="⚠️ 确认删档", font_size=18, bold=True, size_hint_y=None, height=30)
        content.add_widget(lbl)
        
        warn_lbl = Label(text="此操作将清除所有数据，且不可恢复！",
                        font_size=13, color=get_color_from_hex("#FF4D4F"), size_hint_y=None, height=25)
        content.add_widget(warn_lbl)
        
        btn_row = BoxLayout(size_hint_y=None, height=40, spacing=10)
        confirm_btn = Button(text="确认删档", background_color=get_color_from_hex("#FF4D4F"),
                            color=[1,1,1,1], bold=True, border_radius=[12,])
        confirm_btn.bind(on_release=lambda x: self.reset_all_data())
        close_btn = Button(text="取消", background_color=get_color_from_hex("#DDDDDD"),
                          color=get_color_from_hex("#333333"), border_radius=[12,])
        close_btn.bind(on_release=lambda x: popup.dismiss())
        btn_row.add_widget(confirm_btn)
        btn_row.add_widget(close_btn)
        content.add_widget(btn_row)
        
        popup = Popup(title='', content=content, size_hint=(0.8, None), height=220,
                    background_color=[1,1,1,1], separator_height=0)
        popup.open()
    
    def reset_all_data(self):
        """重置所有数据"""
        self.app.expenses = []
        self.app.storage_items = []
        self.app.todo_items = []
        self.app.diaries = []
        self.app.logs = []
        self.app.save_all_data()
        self.app.add_log("警告：所有数据已清除！")
        self.switch_tab('finance')


class PRTSKivyApp(App):
    """Kivy应用入口"""
    def build(self):
        # 设置窗口大小（桌面调试用）
        Window.size = (400, 700)
        
        self.prts_app = PRTSApp()
        return MainScreen(self.prts_app)


if __name__ == '__main__':
    PRTSKivyApp().run()
