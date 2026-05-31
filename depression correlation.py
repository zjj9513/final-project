import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns

# 1. 讀取 CSV 檔案
file_path = "Teen_Mental_Health_Dataset.csv"
df = pd.read_csv(file_path)

# 2. 資料預處理：將文字標籤轉為數值，才能納入相關性計算
social_mapping = {"low": 1, "medium": 2, "high": 3}
df["social_interaction_level"] = df["social_interaction_level"].map(
    social_mapping
)

# 3. 指定要跟抑鬱傾向比較的個別項目（排除變數本身與人口變數 age, gender）
compare_columns = [
    "daily_social_media_hours",
    "sleep_hours",
    "screen_time_before_sleep",
    "academic_performance",
    "physical_activity",
    "social_interaction_level",
    "stress_level",
    "anxiety_level",
    "addiction_level",
]

# 4. 計算所有欄位的相關係數矩陣，並單獨抽取出與 'depression_label' 的相關係數
# .drop('depression_label') 是為了移除抑鬱標籤自己跟自己對比（必然是 1.0）的格子
dep_corr = df[compare_columns + ["depression_label"]].corr()["depression_label"]
dep_corr = dep_corr.drop("depression_label")

# 5. 將結果轉換為 DataFrame並由大到小排序，方便畫圖
corr_df = pd.DataFrame({"Correlation": dep_corr}).sort_values(
    by="Correlation", ascending=False
)

# 6. 設定繪圖風格與中文字型
sns.set_theme(style="whitegrid")
plt.rcParams["font.sans-serif"] = ["Microsoft JhengHei"]
plt.rcParams["axes.unicode_minus"] = False

# 7. 建立畫布
plt.figure(figsize=(10, 6))

# 8. 繪製橫向條形圖 (Horizontal Bar Plot)
# 正相關用紅色（增加抑鬱風險），負相關用藍色（降低抑鬱風險 / 保護因子）
colors = [
    "#C44E52" if x >= 0 else "#4C72B0" for x in corr_df["Correlation"]
]
sns.barplot(
    x="Correlation",
    y=corr_df.index,
    data=corr_df,
    palette=colors,
    hue=corr_df.index,
    legend=False,
)

# 9. 在條形圖的柱子末端加上具體的數字標籤
for i, val in enumerate(corr_df["Correlation"]):
    align = "left" if val >= 0 else "right"
    offset = 0.005 if val >= 0 else -0.005
    plt.text(
        val + offset,
        i,
        f"{val:.3f}",
        va="center",
        ha=align,
        fontsize=10,
        weight="bold",
    )

# 10. 優化圖表外觀與標籤
plt.axvline(x=0, color="black", linestyle="-", linewidth=1)  # 畫一條 Y 軸基準線 (0)
plt.xlim(-0.25, 0.25)  # 限制 X 軸範圍，讓圖表聚焦在主要波動區間
plt.title(
    "個別項目與『抑鬱心理傾向』之相關係數強弱對比圖", fontsize=14, pad=15, weight="bold"
)
plt.xlabel("皮爾森相關係數 (Correlation Coefficient)", fontsize=11)
plt.ylabel("個別項目 / 行為與心理指標", fontsize=11)

# 修改 Y 軸文字為好讀的中文名稱
chinese_labels = {
    "sleep_hours": "睡眠時數",
    "addiction_level": "社群成癮程度",
    "anxiety_level": "焦慮指數",
    "stress_level": "壓力指數",
    "daily_social_media_hours": "每日社群媒體時數",
    "screen_time_before_sleep": "睡前螢幕時間",
    "physical_activity": "身體活動量/運動",
    "social_interaction_level": "現實社交程度",
    "academic_performance": "學業表現 (GPA)",
}
current_ytick_labels = [label.get_text() for label in plt.gca().get_yticklabels()]
new_ytick_labels = [
    chinese_labels.get(label, label) for label in current_ytick_labels
]
plt.gca().set_yticklabels(new_ytick_labels)

plt.tight_layout()
plt.show()