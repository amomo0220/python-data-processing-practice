#!/usr/bin/env python3
"""CSV を集計して data/output.json に出力するスクリプト。

実装方針:
- ヘッダ必須（1行目はヘッダとして読み飛ばす）
- エラー出力は `logging` を使用する
- 出力先は固定で `data/output.json`（上書き）
"""

from __future__ import annotations

import argparse
import csv
import json
import logging
import os
import sys
from typing import Dict


def setup_logging() -> None:
    """ログ出力の初期設定（エラーを標準エラーへ出す）。"""
    logging.basicConfig(level=logging.ERROR, format="%(levelname)s: %(message)s")


def parse_args() -> argparse.Namespace:
    """コマンド引数を解析する。入力ファイルのパスを必須で受け取る。"""
    p = argparse.ArgumentParser(description="CSVを集計して data/output.json に出力します。")
    p.add_argument("input", help="入力CSVファイルのパス（ヘッダ必須）")
    return p.parse_args()


def read_and_aggregate(csv_path: str) -> Dict[str, float]:
    """CSV を読み、category ごとに amount を合計して辞書で返す。

    期待される列順: user_id, amount, category
    ヘッダは読み飛ばす。エラーがあれば logging.error して終了する。
    """
    totals: Dict[str, float] = {}

    if not os.path.exists(csv_path):
        logging.error("入力ファイルが見つかりません: %s", csv_path)
        sys.exit(1)

    try:
        with open(csv_path, newline="", encoding="utf-8") as f:
            # ヘッダ行を利用して列を参照する（列順に依存しない）
            reader = csv.DictReader(f)
            if not reader.fieldnames:
                logging.error("入力ファイルが空です（ヘッダ行が必要です）: %s", csv_path)
                sys.exit(1)

            # ヘッダ名を正規化して amount / category 列を見つける
            normalized_names = {name.strip().lower(): name for name in reader.fieldnames}
            def find_header(target: str) -> str | None:
                return normalized_names.get(target)

            amount_header = find_header("amount")
            category_header = find_header("category")
            if not amount_header or not category_header:
                logging.error("ヘッダに 'amount' または 'category' が見つかりません: %s", reader.fieldnames)
                sys.exit(1)

            for lineno, row in enumerate(reader, start=2):
                # DictReader は不足列を空文字で返すことがある
                amount_str = row.get(amount_header, "")
                category = row.get(category_header, "")
                if category == "":
                    logging.error("行%d: category が空です: %s", lineno, row)
                    sys.exit(1)

                try:
                    amount = float(amount_str)
                except (ValueError, TypeError):
                    logging.error("行%d: amount が数値ではありません: %s", lineno, amount_str)
                    sys.exit(1)

                totals[category] = totals.get(category, 0.0) + amount
    except OSError as e:
        logging.error("入力ファイルを開けません: %s (%s)", csv_path, e)
        sys.exit(1)

    return totals


def write_output(data: Dict[str, float], out_path: str) -> None:
    """結果を JSON として書き込む。data ディレクトリが存在しない場合はエラー扱いとする。"""
    out_dir = os.path.dirname(out_path)
    if out_dir and not os.path.isdir(out_dir):
        logging.error("出力先ディレクトリが存在しません: %s", out_dir)
        sys.exit(1)

    # 整数値は int 表示に変換して見やすくする
    def normalize(v: float):
        return int(v) if float(v).is_integer() else v

    normalized = {k: normalize(v) for k, v in data.items()}

    try:
        with open(out_path, "w", encoding="utf-8") as wf:
            json.dump(normalized, wf, ensure_ascii=False, indent=2)
    except OSError as e:
        logging.error("出力ファイルを書き込めません: %s (%s)", out_path, e)
        sys.exit(1)


def main() -> None:
    """スクリプトのメイン処理。引数解析→集計→フィルタ→出力を行う。"""
    setup_logging()
    args = parse_args()
    input_path = args.input
    output_path = os.path.join("data", "output.json")

    totals = read_and_aggregate(input_path)

    # 合計が1000以上のカテゴリだけ残す
    filtered = {k: v for k, v in totals.items() if v >= 1000}
    if not filtered:
        logging.error("合計が1000以上のcategoryがありません")
        sys.exit(1)

    write_output(filtered, output_path)
    print(f"出力しました: {output_path}")


if __name__ == "__main__":
    main()
