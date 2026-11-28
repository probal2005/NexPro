# 12. Dictionary ও nested records

[← আগের পাঠ](11-lists.md) · [কোর্স সূচি](README.md) · [পরের পাঠ →](13-functions.md)

Dictionary-তে key দিয়ে value পড়া বা বদলানো যায়।

## ধরন ও সিনট্যাক্স

| ধরন | সিনট্যাক্স | সংজ্ঞা |
|---|---|---|
| Literal | `{"sku": "A-01"}` | নামযুক্ত entry তৈরি |
| Update | `item["stock"] = 4` | entry যোগ বা বদল |
| keys | `keys(item)` | প্রবেশের ক্রমে key-এর list |
| get | `get(item, "stock", 0)` | key না থাকলে fallback |
| Nested | `item["counts"][0]` | একই record-এ list বা dictionary রাখে |

## কখন এবং কেন ব্যবহার করবে

পণ্যের SKU, স্টক ও ইতিহাস একটি রেকর্ডে রাখো।

**সুবিধা।** Index মুখস্থ করার বদলে অর্থপূর্ণ key ব্যবহার করা যায়।

**সীমাবদ্ধতা ও সাধারণ ভুল।** সরাসরি অনুপস্থিত key পড়লে error। একই key পুনরায় বসালে সর্বশেষ মান থাকে।

## চালিয়ে দেখো

কোডটি [Playground](https://nexpro-playground.vercel.app/)-এ পেস্ট করে **Run code** চাপো। [উদাহরণের .pa ফাইল](examples/12-dictionaries.pa)

```text
item = {"sku": "A-01", "counts": [2, 4]}
item["counts"][0] = 3
say item["sku"]
say item["counts"][0]
say len(keys(item))
say get(item, "minimum", 0)
```

**প্রত্যাশিত ফল**

```text
A-01
3
2
0
```

## অনুশীলন

minimum = 5 যোগ করে একই get আবার চালাও।

<details>
<summary>উত্তর দেখো</summary>

`item["minimum"] = 5` দিলে `5`।

</details>

[← আগের পাঠ](11-lists.md) · [কোর্স সূচি](README.md) · [পরের পাঠ →](13-functions.md)
