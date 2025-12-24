from typing import Iterable
import pandas as pd


# 15分遅れ
def get_kabutan_stocks(
    url: str = "https://kabutan.jp/tansaku/?mode=2_0311&dispmode=normal",
    markets: Iterable[str] | None = ["東Ｐ", "東Ｓ", "東Ｇ", "東Ｅ"],
    volume: int = 150_000,
) -> pd.DataFrame:
    """
    株探（kabutan）の探索ページから銘柄一覧を取得する

    Args:
        url: 出来高急増の銘柄（デフォルトクエリパラメータ解説: "mode=2_0311" = 出来高急増, "dispmode=normal" = 表示モード）
        markets: 許可する市場コード（例: ["東Ｐ", "東Ｓ", "東Ｇ", "東Ｅ"]）。None の場合はフィルタしない
        volume: 出来高の下限

    Returns:
        市場で絞り込まれた、出来高急増銘柄の一覧
    """
    # HTML内の table をすべて DataFrame として取得
    # [2]に今回欲しい「出来高急増銘柄」がある。
    df = pd.read_html(url)[2]

    # Unnamed 列を削除
    df = df.loc[:, ~df.columns.str.contains("^Unnamed")]

    # カラム名を正規化
    df = df.rename(
        columns={
            "出来高 前日比率": "出来高前日比率",
            "ＰＥＲ": "PER",
            "ＰＢＲ": "PBR",
        }
    )

    for col in ["PER", "PBR", "利回り"]:
        df[col] = pd.to_numeric(df[col], errors="coerce")

    # 必要な列だけ残す（列順も固定）
    df = df[["コード", "銘柄名", "市場", "株価", "前日比", "出来高", "出来高前日比率", "PER", "PBR", "利回り"]]

    # 市場で絞る
    if markets is not None:
        df = df[df["市場"].isin(markets)]

    # 出来高で絞る
    df = df[df["出来高"] >= volume]

    # 株価がプラスのものだけに絞る。
    df = df[df["前日比"] > 0]

    return df


if __name__ == "__main__":
    df = get_kabutan_stocks()
    print(
        df.to_string(
            index=False,
            max_rows=20,
            max_cols=None,
        )
    )
    df.to_csv("logs/kabutan_ranking.csv", index=False)
