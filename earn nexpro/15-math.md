# 15. std/math — পরম মান, rounding ও বর্গমূল

[← আগের পাঠ](14-imports.md) · [কোর্স সূচি](README.md) · [পরের পাঠ →](16-json.md)

NexPro-এর standard math module-এ তিনটি function আছে।

## ধরন ও সিনট্যাক্স

| ধরন | সিনট্যাক্স | সংজ্ঞা |
|---|---|---|
| পরম মান | `math.abs(-7)` | চিহ্ন ছাড়া সংখ্যার মান |
| Rounding | `math.round(12.346, 2)` | নির্দিষ্ট দশমিক ঘর পর্যন্ত round |
| বর্গমূল | `math.sqrt(81)` | অঋণাত্মক সংখ্যার square root |

## কখন এবং কেন ব্যবহার করবে

কোটেশন প্রদর্শনে round ও স্টক পার্থক্যের আকার বের করতে abs ব্যবহার করো।

**সুবিধা।** বহুল ব্যবহৃত হিসাব নিজের function না লিখেই করা যায়।

**সীমাবদ্ধতা ও সাধারণ ভুল।** ঋণাত্মক সংখ্যার বাস্তব বর্গমূল এই ফাংশনে পাওয়া যায় না। Float rounding টাকা-পয়সার exact storage-এর বিকল্প নয়।

## চালিয়ে দেখো

কোডটি [Playground](https://nexpro-playground.vercel.app/)-এ পেস্ট করে **Run code** চাপো। [উদাহরণের .pa ফাইল](examples/15-math.pa)

```text
import "std/math" as math
say math.abs(-7)
say math.round(12.346, 2)
say math.sqrt(81)
```

**প্রত্যাশিত ফল**

```text
7
12.35
9.0
```

## অনুশীলন

144-এর বর্গমূল দেখাও।

<details>
<summary>উত্তর দেখো</summary>

`say math.sqrt(144)` থেকে `12.0`।

</details>

[← আগের পাঠ](14-imports.md) · [কোর্স সূচি](README.md) · [পরের পাঠ →](16-json.md)
