# -*- coding:utf-8 _*-  
""" 
@author:Administrator
@file: query_strings.py
@time: 2018/12/17
"""
# 基础字段插入语句
query_string1 = '''
INSERT INTO 
estate_expect_deal_price_params_data_test(city,"provinceCode","citySpLp","provinceSpLp",dom,"listingCount","soldCount","createdDate","floatingValue")
(select 
td.city as city,
nt.province as "provinceCode",
td.selling_to_listing_price_ratio AS "citySpLp",
td.selling_to_listing_price_ratio AS "provinceSpLp",


td.average_days_on_market AS dom,

td.new_listings AS "listingCount",
td.homes_sold AS "soldCount",
td."createdDate",
2



from trend td
LEFT JOIN 
(
SELECT *
FROM province_city_map
) nt
ON td.city = nt.city)
'''

#后续字段插入语句
query_string2 = '''
UPDATE estate_expect_deal_price_params_data_test
SET "provinceSpLp"=
(SELECT AVG(CAST("citySpLp" AS FLOAT)
FROM estate_expect_deal_price_params_data_test 
where "provinceCode"='ON') AS
WHERE "provinceCode"='ON'

'''

# 获取省份的数据：可以通过citySpLp或者是provinceSpLp都可以
query_string3 = '''
SELECT AVG(CAST("citySpLp" AS FLOAT))
FROM estate_expect_deal_price_params_data_test 
where "provinceCode"='ON'
AND "createdDate" =date(now())

'''
'''
SELECT AVG(CAST("provinceSpLp" AS FLOAT))
FROM estate_expect_deal_price_params_data
where city=NULL
AND "provinceCode"!=NULL
'''
# 省份数据的插入
sql_string7 = '''
INSERT INTO estate_expect_deal_price_params_data_test("provinceCode","provinceSpLp","listingCount","soldCount",dom,"createdDate")
(
select
'ON',
CAST(sum(CAST("citySpLp" as FLOAT)*CAST("soldCount" AS FLOAT))/sum(CAST("soldCount" as FLOAT)) AS DECIMAL(10,2)) AS "provinceSpLp" ,
0,
sum("soldCount") AS "soldCount",
cast(AVG(CAST(dom AS FLOAT)) AS decimal(10,0)) AS dom,
date(now())


FROM estate_expect_deal_price_params_data_test
where city !=''
AND city IS NOT NULL
AND "createdDate"=date(now())
AND "provinceCode"='ON')
'''
# 国家数据的插入？
sql_string8 = '''
INSERT INTO estate_expect_deal_price_params_data_test("soldCount",dom,"createdDate",country,"countrySpLp")
(SELECT 
SUM("soldCount") AS "soldCount",
CAST(AVG(dom) AS decimal(10,0)) as dom,
date(now()) as "createdDate",
'Canada' AS country,
CAST(AVG(CAST("provinceSpLp" AS FLOAT)) AS DECIMAL(10,2))AS "countrySpLp"

FROM estate_expect_deal_price_params_data_test
where 
-- 这里可能会有bug
-- city =''
city IS NULL
AND "createdDate"=date(now())
)
'''
'''
需要的插入字段：
1：省份
    省份的获取方式：
        查询插入的表然通过日期，然后去除循环遍历cursor获取省份存入到list中，set之后然后在循环，这时候省份就可以插入了；
    2：然后是关于    provinceSpLp 的获取：（他是通过平均获取的）# 获取省份的数据：可以通过citySpLp或者是provinceSpLp都可以，约束是通过时间和身份约束的；
    3：
'''