async def calculate_duration(data: dict[str, str]) -> int | None:
    period_multipliers = {
        "⏳ 1 месяц": 1,
        "⏳ 3 месяца": 3,
        "⏳ 6 месяцев": 6,
    }
    period = data.get("period") or ""
    months = period_multipliers.get(period)
    return months


async def calculate_price(data: dict[str, str]) -> float | None:
    price = 0.0
    country_prices = {
        "🇫🇮 Финляндия": 15,
        "🇫🇷 Франция": 15,
        "🇺🇸 США": 5,
        "🇮🇳 Индия": 5,
    }
    vpn_type_prices = {
        "🛡️ OpenVPN": 5,
        "🛡️ VLESS": 15,
    }
    traffic_prices = {
        "⚡ 50 mb/s": 110,
        "🚀 1.0 gb/s": 220,
    }

    country = data.get("country") or ""
    vpn_type = data.get("vpn_type") or ""
    traffic = data.get("traffic") or ""
    months = await calculate_duration(data)
    if months:
        base = (
            country_prices.get(country, 0)
            + vpn_type_prices.get(vpn_type, 0)
            + traffic_prices.get(traffic, 0)
        )
        ip_price = 0
        if months == 1:
            ip_price = 60
        elif months == 3:
            ip_price = 30
        price = float((base * months + ip_price) * 1.1)

        return price
    return None


async def calculate_extend_order_price(
    old_price: float, old_months: int, data: dict[str, str]
):
    months = await calculate_duration(data)
    if months:
        old_price_per_month = old_price / old_months
        new_price = old_price_per_month * months
        return new_price
    return None
