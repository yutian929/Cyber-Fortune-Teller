import sxtwl  # 生辰天文历库
from geopy.geocoders import Nominatim

# 天干、地支表（供字符映射使用）
TIANGAN = ["甲", "乙", "丙", "丁", "戊", "己", "庚", "辛", "壬", "癸"]
DIZHI = ["子", "丑", "寅", "卯", "辰", "巳", "午", "未", "申", "酉", "戌", "亥"]

# 计算真太阳时的偏差
def calculate_time_difference(longitude, standard_longitude=116.4):
    """
    计算经度差并返回对应的时间差，单位：分钟
    :param longitude: 出生地点的经度
    :param standard_longitude: 标准经度（默认北京为116.4度）
    :return: 经度差所对应的时间差，单位：分钟
    """
    longitude_diff = longitude - standard_longitude
    time_diff_minutes = longitude_diff * 4  # 每1度经度差大约对应4分钟
    return time_diff_minutes


# 使用 geopy 获取城市经度
def get_city_longitude(city_name):
    geolocator = Nominatim(user_agent="bazi_calculator")
    location = geolocator.geocode(city_name)

    if location:
        return location.longitude
    else:
        raise ValueError(f"未能找到 {city_name} 的经度信息。")


def calc_bazi(birth_city, year, month, day, hour):
    """计算生辰八字并返回结果"""
    try:
        # 1. 根据城市获取经度
        longitude = get_city_longitude(birth_city)

        # 2. 计算经度差并修正为真太阳时
        time_diff = calculate_time_difference(longitude)

        # 3. 使用 sxtwl 进行阳历 -> 阴历 + 干支 计算
        lunar_day = sxtwl.fromSolar(year, month, day)  # 修改这里，只传递年、月、日

        # 4. 获取年、月、日的干支
        year_gz = lunar_day.getYearGZ()  # 年干支
        month_gz = lunar_day.getMonthGZ()  # 月干支
        day_gz = lunar_day.getDayGZ()  # 日干支

        # 获取时柱：根据日干 + 小时计算
        # 使用真太阳时修正出生时辰
        adjusted_hour = hour + time_diff / 60  # 修正后的小时

        # 确保小时数在0-23之间
        adjusted_hour = adjusted_hour % 24

        hour_gz = sxtwl.getShiGz(day_gz.tg, int(adjusted_hour))

        # 5. 映射干支为文字
        y_tg = TIANGAN[year_gz.tg]  # 年天干
        y_dz = DIZHI[year_gz.dz]  # 年地支
        m_tg = TIANGAN[month_gz.tg]  # 月天干
        m_dz = DIZHI[month_gz.dz]  # 月地支
        d_tg = TIANGAN[day_gz.tg]  # 日天干
        d_dz = DIZHI[day_gz.dz]  # 日地支
        h_tg = TIANGAN[hour_gz.tg]  # 时天干
        h_dz = DIZHI[hour_gz.dz]  # 时地支

        # 6. 拼接四柱八字
        bazi_str = f"{y_tg}{y_dz}  {m_tg}{m_dz}  {d_tg}{d_dz}  {h_tg}{h_dz}"

        return bazi_str
    except Exception as e:
        return f"出错了：{e}"


if __name__ == "__main__":
    # 测试
    birth_city = "吉安"  # 出生城市
    year = 2002
    month = 11
    day = 21
    hour = 9

    result = calc_bazi(birth_city, year, month, day, hour)
    print("生辰八字：", result)
