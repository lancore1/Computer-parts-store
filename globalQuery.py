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
QUERY_SUPPLY = """
    SELECT prod_id,
        prod_name,
        prod_model, 
        prod_spec, 
        categ_name, 
        vend_name,  
        sup_name, 
        prod_quantity
    FROM Get_all_suppl
    """
QUERY_SUPPLIER = "SELECT DISTINCT supplier_name FROM supplier"
QUERY_VENDOR = "SELECT DISTINCT vendor_name from vendor"