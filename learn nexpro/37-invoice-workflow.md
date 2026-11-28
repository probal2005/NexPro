# 37. Capstone — publish a validated invoice tool

[← Previous lesson](36-nested-records.md) · [Course index](README.md)

Build a shareable tool that imports invoices, applies a percentage discount,
and downloads the accepted invoices. Use NexPro 4.9.1 or later.

## Build the workflow

1. **Declare a typed record.** In [invoice_lab.pa](examples/invoice_lab.pa),
   `Invoice` stores whole cents. The `balanced` rule keeps the net, gross and
   discount consistent.
2. **Process each row.** CSV cells arrive as text. Convert `gross` with
   `int()` and catch errors inside the loop so later rows can still run.
3. **Update related values together.** The new discount and net amount would
   violate the rule if assigned separately. Pass them to `records.update()`
   in one call.
4. **Publish the form.** The [entry program](examples/37-invoice-workflow.pa)
   calls the form declared in the aliased module. You can reuse that module
   in another tool.

## Try it

1. Open the [Playground](https://nexpro-playground.vercel.app/) and paste the
   [entry program](examples/37-invoice-workflow.pa) into the editor.
2. Under **Inputs & files**, attach [invoice_lab.pa](examples/invoice_lab.pa)
   in **Module files**, then select **Preview tool**.
3. Upload [invoice-sample.csv](examples/invoice-sample.csv) in the generated
   form. Keep the discount at 10 and select **Calculate**.
4. Use **More → Share tool** and open the link in a new tab. Select **Start
   tool** and upload the sample again. The link contains the code and module.

The tool accepts two rows and reports `INV-002 (invalid_integer)`. The
downloaded `invoices.csv` contains the following data.

```csv
number,gross,discount,net
INV-001,1800,180,1620
INV-003,1200,120,1080
```

## Exercise

Run the same file with a 25% discount. What net amounts do you get?

<details>
<summary>Show the answer</summary>

The first invoice is 1,350 cents and the last is 900 cents. The invalid row
is still reported and skipped.

</details>
