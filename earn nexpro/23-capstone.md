# 23. শেষ প্রজেক্ট — স্টক থেকে পুনঃঅর্ডার

[← আগের পাঠ](22-cli-debug-test.md) · [কোর্স সূচি](README.md)

একটি পূর্ণ workflow-তে input, validation, loop, dictionary, summary ও export একসঙ্গে থাকে।

## ধরন ও সিনট্যাক্স

| ধরন | সিনট্যাক্স | সংজ্ঞা |
|---|---|---|
| Input | `csv_field()` | SKU ও স্টকের টেবিল পড়ার ঘর |
| Rule | `if stock <= minimum` | কোন আইটেম পুনঃঅর্ডার হবে |
| Collection | list of dictionaries | আউটপুট সারি রাখে |
| Export | `csv.stringify()` ও `download_csv()` | নামসহ report দেয় |

## কখন এবং কেন ব্যবহার করবে

Preview tool-এ sample-stock.csv আপলোড করে Calculate চাপো। এরপর পড়ার জন্য রিপোজিটরির পূর্ণ Inventory Reorder উদাহরণে যাও।

**সুবিধা।** শিক্ষার্থী একটি বাস্তব কাজে language component-গুলোর সংযোগ বুঝতে পারে।

**সীমাবদ্ধতা ও সাধারণ ভুল।** এই ছোট সংস্করণ অখণ্ড সংখ্যার sample ধরে। পূর্ণ Inventory Reorder উদাহরণে ভুল সংখ্যার জন্য সারির নম্বরসহ feedback আছে।

## চালিয়ে দেখো

কোডটি [Playground](https://nexpro-playground.vercel.app/)-এ পেস্ট করে **Preview tool** চাপো। [উদাহরণের .pa ফাইল](examples/23-capstone.pa)

[Sample CSV](examples/sample-stock.csv) · [পূর্ণ Inventory Reorder সোর্স](../examples/tool_inventory.pa) · [লাইভ টুল](https://nexpro-playground.vercel.app/tool.html?example=inventory)

```text
import "std/csv" as csv
file = csv_field("Stock CSV", ["sku", "stock", "minimum", "target"])
if file != ""
    orders = []
    for item in csv.parse(file)
        stock = int(item["stock"])
        minimum = int(item["minimum"])
        target = int(item["target"])
        assert stock >= 0 and minimum >= 0 and target > minimum
        if stock <= minimum
            append(orders, {"sku": item["sku"], "quantity": target - stock})
        end
    end
    result("Reorder count", len(orders))
    if len(orders) > 0
        download_csv("reorder.csv", csv.stringify(orders))
    else
        download_csv("reorder.csv", "sku,quantity")
    end
end
```

**প্রত্যাশিত ফল**

```text
Reorder count: 1
reorder.csv: sku,quantity তারপর A-01,8
```

## অনুশীলন

B-02-এর স্টক ২ করে আবার চালাও।

<details>
<summary>উত্তর দেখো</summary>

দুইটি অর্ডার হবে। B-02-এর quantity হবে `9 - 2 = 7`।

</details>

[← আগের পাঠ](22-cli-debug-test.md) · [কোর্স সূচি](README.md)
