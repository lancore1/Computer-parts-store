# Big Query 
# QUERY_TAB = """
#             SELECT 
#                 p.product_id,
#                 p.product_name,
#                 p.product_model,
#                 GROUP_CONCAT(DISTINCT ps.productSpec_value SEPARATOR '/'),
#                 c.category_name,
#                 v.vendor_name,
#                 supp.supplier_name,
#                 p.product_quantity,
#                 p.product_price
#             FROM product p
#             JOIN product_specification ps ON p.product_id = ps.product_id
#             JOIN category_specification cs ON cs.categorySpec_id = ps.categorySpec_id
#             JOIN category c ON c.category_id = cs.category_id
#             JOIN vendor v USING(vendor_id)
#             JOIN supplier_product sp ON sp.product_id=p.product_id
#             JOIN supply suppl ON suppl.supply_id=sp.supply_id
#             JOIN supplier supp ON suppl.supplier_id=supp.supplier_id
#             GROUP BY
#                 p.product_id,
#                 p.product_name,
#                 p.product_model,
#                 c.category_name,
#                 v.vendor_name,
#                 supp.supplier_name,
#                 p.product_quantity,
#                 p.product_price; 
#         """
QUERY_TAB = """
    SELECT prod_id,
        prod_name,
        prod_model, 
        prod_spec, 
        categ_name, 
        vend_name,  
        sup_name, 
        prod_quantity, 
        prod_price
    FROM Get_all_prod
    """