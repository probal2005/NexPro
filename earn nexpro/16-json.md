# 16. std/json — JSON পড়া ও লেখা

[← আগের পাঠ](15-math.md) · [কোর্স সূচি](README.md) · [পরের পাঠ →](17-csv.md)

JSON হলো সিস্টেমের মধ্যে আদানপ্রদানের একটি টেক্সট ফরম্যাট।

## ধরন ও সিনট্যাক্স

| ধরন | সিনট্যাক্স | সংজ্ঞা |
|---|---|---|
| Parse | `json.parse(text)` | JSON string থেকে value তৈরি করে |
| Stringify | `json.stringify(value)` | NexPro value থেকে JSON string বানায় |

## কখন এবং কেন ব্যবহার করবে

রিপোর্ট বা form input-এর structured record অন্য সিস্টেমে পাঠানোর জন্য ব্যবহার করো।

**সুবিধা।** Nested data এবং Unicode নাম সংরক্ষণ করা যায়।

**সীমাবদ্ধতা ও সাধারণ ভুল।** ভুল JSON বা non-finite number error দেয়। JSON-এ key ও string-এ double quote দরকার।

## চালিয়ে দেখো

কোডটি [Playground](https://nexpro-playground.vercel.app/)-এ পেস্ট করে **Run code** চাপো। [উদাহরণের .pa ফাইল](examples/16-json.pa)

```text
import "std/json" as json
record = json.parse('{"name": "আদা", "score": 85}')
say record["name"]
say json.stringify([record["score"], 90])
```

**প্রত্যাশিত ফল**

```text
আদা
[85, 90]
```

## অনুশীলন

score ৯০ করে পুরো রেকর্ড JSON হিসেবে দেখাও।

<details>
<summary>উত্তর দেখো</summary>

`record["score"] = 90` তারপর `say json.stringify(record)`।

</details>

[← আগের পাঠ](15-math.md) · [কোর্স সূচি](README.md) · [পরের পাঠ →](17-csv.md)
