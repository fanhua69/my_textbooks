正则表达式行尾锚点必须用 $，严禁写成 \$（否则匹配的是字面量 $ 字符）。
命令行或 python3 -c 拼接 f-string 时，避免在表达式内部写 \"。
修改 split_chapter.py 后，顺手核对 re.match 行尾是否带 \$。