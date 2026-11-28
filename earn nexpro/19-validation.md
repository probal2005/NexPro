# 19. Validation, assertion ও runtime error

[← আগের পাঠ](18-forms.md) · [কোর্স সূচি](README.md) · [পরের পাঠ →](20-csv-tools.md)

Validation ভুল ইনপুটের কারণ ব্যাখ্যা করে। Assertion প্রোগ্রামের প্রয়োজনীয় শর্ত পরীক্ষা করে।

## ধরন ও সিনট্যাক্স

| ধরন | সিনট্যাক্স | সংজ্ঞা |
|---|---|---|
| Assertion | `assert quantity >= 0` | ব্যর্থ হলে runtime error |
| Field validation | `field_check(label, condition, message)` | ব্রাউজারে সংশ্লিষ্ট ফিল্ডের পাশে বার্তা |
| Numeric bounds | `number_field("Quantity", 2, 1, 20, 1)` | পূর্ণসংখ্যা ও সীমা যাচাই |
| Stack trace | runtime error-এর file ও line | কোন expression বা call-এ ভুল হয়েছে দেখায় |

## কখন এবং কেন ব্যবহার করবে

খালি নাম, ঋণাত্মক quantity বা সীমার বাইরের মান ধরে ব্যবহারকারীকে কী ঠিক করতে হবে জানাও।

**সুবিধা।** ভুল ডেটা হিসাবের আগেই ধরা যায়।

**সীমাবদ্ধতা ও সাধারণ ভুল।** field_check টার্মিনালে ব্যর্থ হলে error দেয়। 3.6-এ try/catch নেই।

## চালিয়ে দেখো

কোডটি [Playground](https://nexpro-playground.vercel.app/)-এ পেস্ট করে **Preview tool** চাপো। [উদাহরণের .pa ফাইল](examples/19-validation.pa)

```text
name = text_field("Name", "Ada")
quantity = number_field("Quantity", 2, 1, 20, 1)
assert quantity > 0
if field_check("Name", len(trim(name)) > 0, "Enter a name.")
    result("Order", name)
end
```

**প্রত্যাশিত ফল**

```text
Order: Ada
```

## অনুশীলন

Name খালি করে Calculate চাপো।

<details>
<summary>উত্তর দেখো</summary>

Name-এর পাশে `Enter a name.` দেখাবে।

</details>

[← আগের পাঠ](18-forms.md) · [কোর্স সূচি](README.md) · [পরের পাঠ →](20-csv-tools.md)
