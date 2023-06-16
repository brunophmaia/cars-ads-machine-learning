from scripts.attributes_ads_etl import join_dfs, olx_attrs_etl, print_attributes_olx, print_attributes_seminovos, printValuesFromKey, seminovos_attrs_etl, process_completo_final_dataframe
from scripts.join_files import joinFiles
from scripts.brands_models_combo_scraping import executeCombosScraping
from scripts.brands_models_extract import extractBrandsModelAndSaveFile
from scripts.diffs_rename_brands_models import generateModelsDiffs, getDataFrames, printDiffsBrands, renameBrandsAndSaveFile, renameModelsAndSaveFile
from mg_cities.cities import getCitiesProcessed, printCitiesNotInOlx, printCitiesNotInSeminovos
from scripts.values_treatment import removeDuplicates, getDataFrameJoined, outliers, delete_missing_cities, fill_category_missing_values, fill_value_missing_values, separate_brand_model, write_csv

# step 1
joinFiles()
# step 1

# step 2
executeCombosScraping()
extractBrandsModelAndSaveFile()
# step 2

# step 3
df_olx, df_seminovos = getDataFrames('step_2_brands_models_extracted')
printDiffsBrands(df_olx, df_seminovos)
renameBrandsAndSaveFile(df_olx, df_seminovos)
# step 3

# step 4
df_olx, df_seminovos = getDataFrames('step_3_brands_renamed')
generateModelsDiffs(df_olx, df_seminovos)
renameModelsAndSaveFile(df_olx, df_seminovos)
# step 4

# step 5
df_olx, df_seminovos = getDataFrames('step_4_models_renamed')
print_attributes_olx(df_olx,)
print_attributes_seminovos(df_seminovos)
olx_attrs_etl(df_olx)
seminovos_attrs_etl(df_seminovos)
join_dfs(df_olx, df_seminovos)
# step 5

# step 6
df = getDataFrameJoined('step_5_items_extracted')
removeDuplicates(df)
outliers(df)
fill_category_missing_values(df)
fill_value_missing_values(df)
process_completo_final_dataframe(df)
df = delete_missing_cities(df)
write_csv(df)
# step 6