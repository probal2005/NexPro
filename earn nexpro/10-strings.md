# 10. String, index, slice ও text functions

[← আগের পাঠ](09-loops.md) · [কোর্স সূচি](README.md) · [পরের পাঠ →](11-lists.md)

String ক্রমানুসারী Unicode টেক্সট। টেক্সট ভাঙা, পরিষ্কার ও জোড়ার জন্য পাঁচটি বিশেষ built-in আছে।

## ধরন ও সিনট্যাক্স

| ধরন | সিনট্যাক্স | সংজ্ঞা |
|---|---|---|
| trim | `trim("  Ada  ")` | দুই প্রান্তের whitespace সরায় |
| lower | `lower("ADA")` | ছোট হাতের অক্ষর |
| upper | `upper("ada")` | বড় হাতের অক্ষর |
| split | `split("A,B", ",")` | বিভাজক ধরে list বানায় |
| join | `join(["A", "B"], "-")` | সকল string জোড়ে |
| Index ও slice | `name[0]`, `name[0:2]` | এক অক্ষর বা অংশ নেয় |
| Escape | `"A\nB"` | স্ট্রিংয়ের ভিতর নতুন লাইন |

## কখন এবং কেন ব্যবহার করবে

ফর্মের নাম পরিষ্কার, রিপোর্টের লেবেল তৈরি বা সাধারণ কমা দিয়ে আলাদা নাম পড়া।

**সুবিধা।** Unicode টেক্সট ও case conversion দিয়ে একই নিয়মে অনেক নাম প্রসেস করা যায়।

**সীমাবদ্ধতা ও সাধারণ ভুল।** split-এর বিভাজক খালি হতে পারে না। join-এর সব আইটেম string হতে হবে। উদ্ধৃত CSV সেলের জন্য std/csv ব্যবহার করো।

## চালিয়ে দেখো

কোডটি [Playground](https://nexpro-playground.vercel.app/)-এ পেস্ট করে **Run code** চাপো। [উদাহরণের .pa ফাইল](examples/10-strings.pa)

```text
name = trim("  Ada  ")
say lower(name)
say upper(name)
say name[0:2]
say join(split("A,B", ","), " + ")
say "Nex" + "Pro"
```

**প্রত্যাশিত ফল**

```text
ada
ADA
Ad
A + B
NexPro
```

## অনুশীলন

" red,green " থেকে "RED-GREEN" বানাও।

<details>
<summary>উত্তর দেখো</summary>

`upper(join(split(trim(" red,green "), ","), "-"))`।

</details>

[← আগের পাঠ](09-loops.md) · [কোর্স সূচি](README.md) · [পরের পাঠ →](11-lists.md)
