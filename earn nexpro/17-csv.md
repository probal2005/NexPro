# 17. std/csv — টেবিল পড়া ও লেখা

[← আগের পাঠ](16-json.md) · [কোর্স সূচি](README.md) · [পরের পাঠ →](18-forms.md)

CSV-তে প্রথম সারিতে column name থাকে। প্রতিটি data row একটি dictionary হয়ে আসে।

## ধরন ও সিনট্যাক্স

| ধরন | সিনট্যাক্স | সংজ্ঞা |
|---|---|---|
| Parse | `csv.parse(text)` | সেলগুলো string হিসেবে পড়ে |
| Required columns | `csv.parse(text, ["sku", "stock"])` | দরকারি header না থাকলে error দেয় |
| Stringify | `csv.stringify(rows)` | সামঞ্জস্যপূর্ণ dictionary থেকে CSV লেখে |

## কখন এবং কেন ব্যবহার করবে

স্প্রেডশিট এক্সপোর্ট, ইনভেন্টরি বা রিপোর্ট প্রসেস করো।

**সুবিধা।** উদ্ধৃত কমা ও বহু লাইনের সেল পার্স করতে পারে।

**সীমাবদ্ধতা ও সাধারণ ভুল।** সংখ্যার হিসাবের আগে সেলকে int বা float করতে হয়। Duplicate header ও ভুল column count error দেয়।

## চালিয়ে দেখো

কোডটি [Playground](https://nexpro-playground.vercel.app/)-এ পেস্ট করে **Run code** চাপো। [উদাহরণের .pa ফাইল](examples/17-csv.pa)

```text
import "std/csv" as csv
rows = csv.parse('sku,stock
"A, large",4', ["sku", "stock"])
say rows[0]["sku"]
say int(rows[0]["stock"]) + 2
say csv.stringify([{"sku": "A-01", "quantity": 2}])
```

**প্রত্যাশিত ফল**

```text
A, large
6
sku,quantity
A-01,2
```

## অনুশীলন

Header থেকে stock সরাও, কিন্তু required list-এ রাখো।

<details>
<summary>উত্তর দেখো</summary>

`Missing CSV columns: stock` বার্তা পাবে।

</details>

[← আগের পাঠ](16-json.md) · [কোর্স সূচি](README.md) · [পরের পাঠ →](18-forms.md)
