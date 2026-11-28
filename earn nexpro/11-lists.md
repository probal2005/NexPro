# 11. List, array-এর সাধারণ কাজ ও slice

[← আগের পাঠ](10-strings.md) · [কোর্স সূচি](README.md) · [পরের পাঠ →](12-dictionaries.md)

List একটি পরিবর্তনযোগ্য ক্রমানুসারী collection।

## ধরন ও সিনট্যাক্স

| ধরন | সিনট্যাক্স | সংজ্ঞা |
|---|---|---|
| তৈরি | `[10, 20, 30]` | আইটেম সাজিয়ে রাখে |
| Index | `items[0]`, `items[-1]` | প্রথম বা শেষ আইটেম |
| Slice | `items[start:stop:step]` | ক্রম মেনে অংশ নেয়, stop বাদ যায় |
| Update | `items[0] = 8` | আইটেম বদলায় |
| append | `append(items, 40)` | একই list-এর শেষে যোগ |
| range | `range(1, 6, 2)` | দেয় [1, 3, 5] |
| sorted ও reverse | `sorted(items)`, `reverse(items)` | নতুন list দেয় |
| sum, min, max | `sum(items)`, `min(items)`, `max(items)` | সংখ্যার তালিকা থেকে সারাংশ |

## কখন এবং কেন ব্যবহার করবে

স্কোর, অর্ডার বা CSV row-এর মতো ক্রমানুসারী ডেটা।

**সুবিধা।** Index, slice ও loop দিয়ে তালিকা বিশ্লেষণ করা যায়।

**সীমাবদ্ধতা ও সাধারণ ভুল।** সীমার বাইরের index-এ error। min ও max খালি list নেয় না। 3.6-এ আলাদা fixed array বা linked-list built-in নেই।

## চালিয়ে দেখো

কোডটি [Playground](https://nexpro-playground.vercel.app/)-এ পেস্ট করে **Run code** চাপো। [উদাহরণের .pa ফাইল](examples/11-lists.pa)

```text
scores = [70, 85, 100]
scores[0] = 75
append(scores, 80)
say scores[-1]
say scores[0:2]
say sorted(scores)
say reverse(range(1, 4))
say sum(scores)
say min(scores)
say max(scores)
```

**প্রত্যাশিত ফল**

```text
80
[75, 85]
[75, 80, 85, 100]
[3, 2, 1]
340
75
100
```

## অনুশীলন

শেষ দুইটি স্কোর নাও।

<details>
<summary>উত্তর দেখো</summary>

`scores[-2:]` থেকে `[100, 80]`।

</details>

[← আগের পাঠ](10-strings.md) · [কোর্স সূচি](README.md) · [পরের পাঠ →](12-dictionaries.md)
