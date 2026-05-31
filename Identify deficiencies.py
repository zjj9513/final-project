import pandas as pd

# 1. 讀取 CSV 檔案
file_path = "Teen_Mental_Health_Dataset.csv"
df = pd.read_csv(file_path)

# 2. 基礎資訊輸出
print("--- 檔案資料結構基本資訊 ---")
print(f"總資料筆數：{df.shape[0]} 筆")
print(f"總欄位數量：{df.shape[1]} 個\n")

# 3. 檢查缺失值
missing_count = df.isnull().sum()
missing_percentage = (df.isnull().sum() / len(df)) * 100

# 4. 取得數值型欄位的統計資訊（最大、最小、平均、四分位數）
# .describe() 預設會計算 count, mean, std, min, 25%, 50%, 75%, max
# 我們轉置 (.T) 它，方便之後與缺失值表格進行合併
stats_info = df.describe().T

# 5. 將缺失值資訊與統計資訊合併成一張大表格
# 建立一個基礎 DataFrame 包含缺失值
data_report = pd.DataFrame(
    {"缺失值總數 (Total)": missing_count, "百分比 (Percentage %)": missing_percentage}
)

# 將統計資訊合併進來（文字欄位如 gender、platform_usage 統計值會自動填為 NaN）
data_report = data_report.join(stats_info)

# 6. 重新命名部分欄位名稱，讓報告更直覺易讀
data_report = data_report.rename(
    columns={
        "mean": "平均值 (Mean)",
        "min": "最小值 (Min)",
        "25%": "下四分位數 (25%)",
        "50%": "中位數 (50%)",
        "75%": "上四分位數 (75%)",
        "max": "最大值 (Max)",
    }
)

# 7. 調整欄位顯示順序，移除不必要的 std(標準差) 與 count
output_columns = [
    "缺失值總數 (Total)",
    "百分比 (Percentage %)",
    "最小值 (Min)",
    "下四分位數 (25%)",
    "中位數 (50%)",
    "上四分位數 (75%)",
    "最大值 (Max)",
    "平均值 (Mean)",
]
# 確保只輸出我們需要的欄位（排除文字欄位不適用的數值）
final_report = data_report.reindex(columns=output_columns)

print("--- 各欄位完整數據報告 (含缺失值與描述性統計) ---")
print(final_report.to_string())
