# 20. CSV upload ও নামসহ download

[← আগের পাঠ](19-validation.md) · [কোর্স সূচি](README.md) · [পরের পাঠ →](21-sharing.md)

CSV field ব্যবহারকারীর নির্বাচিত ফাইল থেকে টেক্সট দেয়। Download call টেক্সটকে একটি নামযুক্ত CSV হিসেবে দেয়।

## ধরন ও সিনট্যাক্স

| ধরন | সিনট্যাক্স | সংজ্ঞা |
|---|---|---|
| Upload | `csv_field(label, columns, default)` | UTF-8 CSV ও প্রয়োজনীয় column names |
| Guard | `if file != "" … end` | ফাইল না থাকলে বা বৈধ না হলে প্রসেসিং থামায় |
| Export | `download_csv("reorder.csv", text)` | ব্রাউজারে ডাউনলোড বাটন, CLI-তে stdout |

## কখন এবং কেন ব্যবহার করবে

Inventory CSV form-এর মতো টুলে যে কলামগুলো দরকার সেগুলো ঘোষণা করো। Preview tool-এ Stock CSV ঘরে sku,stock header এবং A-01,4 সারি থাকা ফাইল দাও।

**সুবিধা।** ব্যবহারকারী নিজের CSV দিয়ে সরাসরি রিপোর্ট বের করতে পারে।

**সীমাবদ্ধতা ও সাধারণ ভুল।** প্রতি আপলোডে 512 KB এবং এক রান-এর মোট ডাউনলোডে 512 KB সীমা। অনুপস্থিত কলামে ফিল্ডের কাছে ভুল দেখায়।

## চালিয়ে দেখো

কোডটি [Playground](https://nexpro-playground.vercel.app/)-এ পেস্ট করে **Preview tool** চাপো। [উদাহরণের .pa ফাইল](examples/20-csv-tools.pa)

পরীক্ষার জন্য [sample-stock.csv](examples/sample-stock.csv) ব্যবহার করো। ১-সারির ফল দেখতে header এবং শুধু A-01 সারিটি রাখো। সম্পূর্ণ sample চালালে Rows হবে 2।

```text
import "std/csv" as csv
file = csv_field("Stock CSV", ["sku", "stock"])
if file != ""
    rows = csv.parse(file)
    result("Rows", len(rows))
    if len(rows) > 0
        download_csv("stock.csv", csv.stringify(rows))
    end
end
```

**প্রত্যাশিত ফল**

```text
Rows: 1
Download stock.csv বাটন আসে।
```

## অনুশীলন

stock column বাদ দিয়ে একই ফর্মে চালাও।

<details>
<summary>উত্তর দেখো</summary>

ফিল্ডের পাশে `Missing CSV columns: stock`।

</details>

[← আগের পাঠ](19-validation.md) · [কোর্স সূচি](README.md) · [পরের পাঠ →](21-sharing.md)
