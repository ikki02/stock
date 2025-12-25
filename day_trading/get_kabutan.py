import logging
from typing import Iterable

import pandas as pd

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def get_kabutan_pts_stocks(
    url: str = "https://kabutan.jp/warning/pts_night_price_increase",
    markets: Iterable[str] | None = ["東Ｐ", "東Ｓ", "東Ｇ", "東Ｅ"],
    volume: int = 100_000,
) -> pd.DataFrame:
    """
    株探（kabutan）の探索ページから銘柄一覧を取得する

    Args:
        url: PTS市場の株価上昇率ランキングや出来高ランキングのURL
        markets: 許可する市場コード（例: ["東Ｐ", "東Ｓ", "東Ｇ", "東Ｅ"]）。None の場合はフィルタしない
        volume: 出来高の下限

    Returns:
        市場と出来高で絞り込まれた、PTS市場の値上がり銘柄の一覧
    """
    # HTML内のランキング50件を取得する。for文でまわさない場合15件しか取れないため、pageパラメータを回して上位50件を取得する
    dfs = []
    for page in range(1, 3):  # 1〜3 くらいまで試す
        url = f"{url}?dispmode=normal&page={page}"  # デフォルトクエリパラメータ解説: "dispmode=normal" = 表示モード
        table = pd.read_html(url)[2]  # ページ構造によってインデックス調整。# [2]に今回欲しいランキングがある。
        dfs.append(table)
    df = pd.concat(dfs, ignore_index=True)

    # 列が銘柄のマルチインデックスのため、この2段重ねのうち、列名（1番目）だけ残したい
    df.columns = df.columns.get_level_values(1)

    # Unnamed 列を削除
    df = df.loc[:, ~df.columns.str.contains("^Unnamed")]

    # 取得日に依存するカラム名の抽出
    pattern = r"通常取引\s*(\d+)日終値.*"
    day = df.columns.str.extract(pattern, expand=False).dropna()[0]
    logger.info(f"{day}日の終値を取得しています。")

    # カラム名を正規化
    df = df.rename(
        columns={
            f"通常取引 {day}日終値": "株価",
            "株価": "PTS株価",
            f"通常取引 {day}日終値比": f"通常取引{day}日終値比(実数)",
            f"通常取引 {day}日終値比.1": f"通常取引{day}日終値比(率)",
            "ＰＥＲ": "PER",
            "ＰＢＲ": "PBR",
        }
    )

    # 必要な列だけ残す（列順も固定）
    df = df[
        [
            "銘柄名",
            "コード",
            "市場",
            "株価",
            "PTS株価",
            f"通常取引{day}日終値比(実数)",
            f"通常取引{day}日終値比(率)",
            "出来高",
            "PER",
            "PBR",
            "利回り",
        ]
    ]

    for col in ["株価", "PTS株価", "PER", "PBR", "利回り"]:
        df[col] = pd.to_numeric(df[col], errors="coerce")

    # 市場で絞る
    if markets is not None:
        df = df[df["市場"].isin(markets)]

    # 出来高で絞る
    df = df[df["出来高"] >= volume]

    # PTS株価がプラスのものだけに絞る。
    df = df[df[f"通常取引{day}日終値比(実数)"] > 0]

    return df


if __name__ == "__main__":
    df = get_kabutan_pts_stocks(url="https://kabutan.jp/warning/pts_night_price_increase", markets=["東Ｐ", "東Ｓ", "東Ｇ"])
    # df = get_kabutan_pts_stocks(url="https://kabutan.jp/warning/pts_night_volume_ranking")
    print(
        df.to_string(
            index=False,
            max_rows=20,
            max_cols=None,
        )
    )
    df.to_csv("logs/kabutan_ranking.csv", index=False)
