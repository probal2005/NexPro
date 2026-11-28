# 07. Boolean ও logical operators

[← আগের পাঠ](06-comparisons.md) · [কোর্স সূচি](README.md) · [পরের পাঠ →](08-conditionals.md)

একটি বা একাধিক শর্ত থেকে সিদ্ধান্ত বের করতে তিনটি logical operator আছে।

## ধরন ও সিনট্যাক্স

| ধরন | সিনট্যাক্স | সংজ্ঞা |
|---|---|---|
| and | `a and b` | দুই শর্তই সত্য |
| or | `a or b` | অন্তত একটি শর্ত সত্য |
| not | `not a` | শর্ত উল্টায় |
| Truth value | `not []` | খালি list, খালি string, খালি dictionary ও ০ শর্তে মিথ্যা গণ্য হয় |

## কখন এবং কেন ব্যবহার করবে

অর্ডার ছাড়তে স্টক এবং গ্রাহকের অনুমোদন দুটোই পরীক্ষা করো।

**সুবিধা।** Short-circuit-এর কারণে প্রথম শর্তেই ফল জানা গেলে দ্বিতীয় শর্ত চলে না।

**সীমাবদ্ধতা ও সাধারণ ভুল।** and ও or boolean ফেরত দেয়। একাধিক নিয়ম জুড়লে বন্ধনী ও নামযুক্ত ভেরিয়েবল পড়তে সুবিধা দেয়।

## চালিয়ে দেখো

কোডটি [Playground](https://nexpro-playground.vercel.app/)-এ পেস্ট করে **Run code** চাপো। [উদাহরণের .pa ফাইল](examples/07-logic.pa)

```text
stock = 4
approved = true
say stock > 0 and approved
say stock == 0 or not approved
say stock != 0 and 12 / stock > 2
```

**প্রত্যাশিত ফল**

```text
true
false
true
```

## অনুশীলন

stock = 0 করলে শেষ লাইনে কী হবে?

<details>
<summary>উত্তর দেখো</summary>

`false`। ভাগের expression চালানো হবে না।

</details>

[← আগের পাঠ](06-comparisons.md) · [কোর্স সূচি](README.md) · [পরের পাঠ →](08-conditionals.md)
