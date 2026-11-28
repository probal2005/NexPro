# 03. ডেটা টাইপ ও মান

[← আগের পাঠ](02-variables.md) · [কোর্স সূচি](README.md) · [পরের পাঠ →](04-input-output.md)

NexPro-তে ছয় ধরনের মান সরাসরি literal দিয়ে লেখা যায়।

## ধরন ও সিনট্যাক্স

| ধরন | সিনট্যাক্স | সংজ্ঞা |
|---|---|---|
| Integer | `12` | পূর্ণসংখ্যা |
| Float | `7.5` | দশমিক সংখ্যা |
| String | `"আদা"` | টেক্সট |
| Boolean | `true`, `false` | শর্তের মান |
| List | `[3, 4]` | ক্রম অনুযায়ী আইটেম |
| Dictionary | `{"stock": 4}` | নামযুক্ত key–value ডেটা |

## কখন এবং কেন ব্যবহার করবে

আইটেমের সংখ্যা integer, পণ্যের নাম string এবং একই পণ্যের বৈশিষ্ট্য dictionary-তে রাখো।

**সুবিধা।** ডেটার ধরন উদ্দেশ্য অনুযায়ী বেছে নেওয়া যায়।

**সীমাবদ্ধতা ও সাধারণ ভুল।** অপারেশনের সঙ্গে মানের ধরন না মিললে error হতে পারে। Return ছাড়া শেষ হওয়া function-এর ফল None হিসেবে দেখা যায়। আলাদা null literal নেই।

## চালিয়ে দেখো

কোডটি [Playground](https://nexpro-playground.vercel.app/)-এ পেস্ট করে **Run code** চাপো। [উদাহরণের .pa ফাইল](examples/03-data-types.pa)

```text
item = {"name": "Rice", "stock": 4}
say item["name"]
say item["stock"] > 0
say len([4, 5])
```

**প্রত্যাশিত ফল**

```text
Rice
true
2
```

## অনুশীলন

স্টক ০ করে আবার চালাও।

<details>
<summary>উত্তর দেখো</summary>

দ্বিতীয় লাইন `false`।

</details>

[← আগের পাঠ](02-variables.md) · [কোর্স সূচি](README.md) · [পরের পাঠ →](04-input-output.md)
