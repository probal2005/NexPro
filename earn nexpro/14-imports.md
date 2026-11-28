# 14. Import ও module namespace

[← আগের পাঠ](13-functions.md) · [কোর্স সূচি](README.md) · [পরের পাঠ →](15-math.md)

Module হলো পুনর্ব্যবহারযোগ্য সোর্স ফাইল বা স্ট্যান্ডার্ড লাইব্রেরির অংশ।

## ধরন ও সিনট্যাক্স

| ধরন | সিনট্যাক্স | সংজ্ঞা |
|---|---|---|
| সাধারণ import | `import "rules.pa"` | আমদানিকৃত টপ-লেভেল কোড একই scope-এ অন্তর্ভুক্ত হয় |
| Alias | `import "rules.pa" as rules` | একটি স্বতন্ত্র namespace দেয় |
| Member access | `rules.quote(50, 3)` | alias দিয়ে function বা top-level মান পড়ে |
| Standard import | `import "std/math" as math` | NexPro-এর প্রস্তুত মডিউল যোগ করে |

## কখন এবং কেন ব্যবহার করবে

হিসাবের নিয়ম আলাদা ফাইলে রাখো। নিচের demo দুটির জন্য rules.pa নামের ফাইলটি মূল ফাইলের পাশে রাখো বা Playground-এর Module files-এ যোগ করো।

**সুবিধা।** Alias একাধিক ফাইলে একই নাম থাকার সংঘর্ষ কমায়।

**সীমাবদ্ধতা ও সাধারণ ভুল।** Path importing file থেকে relative এবং entry file-এর directory-এর ভেতরে থাকতে হবে। Circular import error দেয়।

## চালিয়ে দেখো

কোডটি [Playground](https://nexpro-playground.vercel.app/)-এ পেস্ট করে **Run code** চাপো। [উদাহরণের .pa ফাইল](examples/14-imports.pa)

সঙ্গে [rules.pa](examples/rules.pa) ফাইলটি লাগবে।

```text
import "rules.pa" as rules
say rules.quote(50, 3)
say rules.currency
```

**প্রত্যাশিত ফল**

```text
150
BDT
```

## অনুশীলন

rules.pa-তে quote function-এ ১০ টাকা সার্ভিস ফি যোগ করো।

<details>
<summary>উত্তর দেখো</summary>

`return price * count + 10` দিলে প্রথম ফল `160`।

</details>

[← আগের পাঠ](13-functions.md) · [কোর্স সূচি](README.md) · [পরের পাঠ →](15-math.md)
