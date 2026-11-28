# 06. Comparison operators

[← আগের পাঠ](05-arithmetic.md) · [কোর্স সূচি](README.md) · [পরের পাঠ →](07-logic.md)

দুই operand-এর সম্পর্ক পরীক্ষা করলে boolean মান পাওয়া যায়।

## ধরন ও সিনট্যাক্স

| ধরন | সিনট্যাক্স | সংজ্ঞা |
|---|---|---|
| সমতা | `==`, `!=` | সমান ও অসমান |
| ছোট | `<`, `<=` | ছোট ও ছোট-সমান |
| বড় | `>`, `>=` | বড় ও বড়-সমান |

## কখন এবং কেন ব্যবহার করবে

স্টক সীমায় পৌঁছেছে কি না বা নম্বর পাস কাট-অফে পৌঁছেছে কি না পরীক্ষা করো।

**সুবিধা।** সীমার সমান মান অন্তর্ভুক্ত হবে কি না চিহ্নেই স্পষ্ট হয়।

**সীমাবদ্ধতা ও সাধারণ ভুল।** একটি comparison expression-এ একটি comparison operator ব্যবহার করো। দুই তুলনা and দিয়ে জুড়তে পারো।

## চালিয়ে দেখো

কোডটি [Playground](https://nexpro-playground.vercel.app/)-এ পেস্ট করে **Run code** চাপো। [উদাহরণের .pa ফাইল](examples/06-comparisons.pa)

```text
stock = 4
say stock == 4
say stock != 4
say stock < 5
say stock <= 4
say stock > 3
say stock >= 5
```

**প্রত্যাশিত ফল**

```text
true
false
true
true
true
false
```

## অনুশীলন

স্টক ৩ থেকে ৬-এর মধ্যে আছে কি না পরীক্ষা করো।

<details>
<summary>উত্তর দেখো</summary>

`stock >= 3 and stock <= 6`।

</details>

[← আগের পাঠ](05-arithmetic.md) · [কোর্স সূচি](README.md) · [পরের পাঠ →](07-logic.md)
