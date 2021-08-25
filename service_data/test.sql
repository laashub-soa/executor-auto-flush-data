-- 用自购报账单更新, 执行完才执行下一个脚本 "用自购修正单更新"
SELECT
/*+ SET_VAR(max_parallel_degree=10) */
    concat(
            'UPDATE delivery_dtl SET buy_qty = ', expense_dtl.qty,
            ',buy_price = ', expense_dtl.buy_price,
            ',buy_amount = ', expense_dtl.buy_amount,
            ' WHERE id = ',
            t1.id,
            ';'
        ) AS updSql
FROM
    delivery_dtl t1
        JOIN expense_apply_dtl expense_dtl on t1.id = expense_dtl.delivery_dtl_id
        JOIN v_expense_apply expense_v on expense_v.id = expense_dtl.expense_apply_id
WHERE
        t1.from_system = 2
  and t1.`status` = 1
-- 排除已有报账的数据
  and not EXISTS (
        SELECT
            1
        from expense_apply_correct_dtl crd
        where t1.id = crd.delivery_dtl_id
    )
  and not(
            t1.buy_qty        = expense_dtl.qty
        and t1.buy_price  = expense_dtl.buy_price
        and t1.buy_amount = expense_dtl.buy_amount
    )