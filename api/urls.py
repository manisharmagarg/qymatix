# from django.conf.urls import patterns, url
from django.urls import path, re_path

from django.contrib.auth.decorators import login_required
# from tokenapi.decorators import token_required
from tokenapi.decorators import token_required
from api import actionsapi
from api import contactsapi
from api import customersapi
from api import dataanalysisapi
from api import insightsapi
from api import salesapi 
from api import usersapi
from api import groupsapi
from api import mapsapi
from api import productsapi
from api import goalsapi 
from api import industryapi
# from api import currenciesapi
# from api import xingapi 
# from webapp import views


urlpatterns = [
    # re_path(r'^doc$', customersapi.apidoc_index, name=u"apidoc"),
    re_path(r'^doc/$', login_required(customersapi.apidoc_index, login_url='/webapp/v1.0/login'), name=u"apidoc"),
    re_path(r'^doc/index/$', login_required(customersapi.apidoc_index, login_url='/webapp/v1.0/login/'), name=u"apidoc"),
    re_path(r'^doc/search/$', login_required(customersapi.apidoc_search, login_url='/webapp/v1.0/login/'), name=u"apidoc"),
    re_path(r'^doc/genindex/$', login_required(customersapi.apidoc_genindex, login_url='/webapp/v1.0/login/'), name=u"apidoc"),
    re_path(r'^doc/introduction/$', login_required(customersapi.apidoc_introduction, login_url='/webapp/v1.0/login'), name=u"apidoc"),
    re_path(r'^doc/customer_functions/$', login_required(customersapi.apidoc_customer_functions, login_url='/webapp/v1.0/login/'), name=u"apidoc"),
    re_path(r'^doc/users_api/$', login_required(usersapi.apidoc_users_api, login_url='/webapp/v1.0/login/'), name=u"apidoc"),
    re_path(r'^doc/actions_api/$', login_required(actionsapi.apidoc_actions_api, login_url='/webapp/v1.0/login/'), name=u"apidoc"),
    re_path(r'^doc/goals_api/$', login_required(goalsapi.apidoc_goals_api, login_url='/webapp/v1.0/login/'), name=u"apidoc"),
    re_path(r'^doc/products_api/$', login_required(productsapi.apidoc_products_api, login_url='/webapp/v1.0/login/'), name=u"apidoc"),
    # re_path(r'^(?P<workspace>\d+)/upload$', login_required(views.upload), name=u"upload"),
    # re_path(r'^(?P<workspace>\d+)/(?P<user>\d+):(?P<token>[-\w\d-]+)/upload$', token_required(views.upload), name=u"upload"),

    # Critters related urls

    # Insights
    re_path(r'^(?P<workspace>\d+)/getinsights$', login_required(insightsapi.getInsights, login_url='/webapp/v1.0/login/'), name=u"apidata"),
    re_path(r'^(?P<workspace>\d+)/getinsights/(?P<account>.*)$', login_required(insightsapi.getInsights, login_url='/webapp/v1.0/login/'), name=u"apidata"),
    re_path(r'^(?P<workspace>\d+)/get_insights$', login_required(insightsapi.get_insights, login_url='/webapp/v1.0/login/'), name=u"apidata"),
    re_path(r'^(?P<workspace>\d+)/get_insights/(?P<account>.*)$', login_required(insightsapi.get_insights, login_url='/webapp/v1.0/login/'), name=u"apidata"),
    re_path(r'^(?P<workspace>\d+)/getCustomerRisk$', login_required(insightsapi.getCustomerRisk, login_url='/webapp/v1.0/login/'), name=u"apidata"),
    re_path(r'^(?P<workspace>\d+)/getCustomerRisk/(?P<account>[-\w ]+)$', login_required(insightsapi.getCustomerRisk, login_url='/webapp/login/'), name=u"apidata"),
    re_path(r'^(?P<workspace>\d+)/getCrossSellingProducts$', login_required(insightsapi.getCrossSellingProducts, login_url='/webapp/v1.0/login/'), name=u"apidata"),
    re_path(r'^(?P<workspace>\d+)/getCrossSellingProducts/(?P<account>.*)$', login_required(insightsapi.getCrossSellingProducts, login_url='/webapp/v1.0/login/'), name=u"apidata"),
    re_path(r'^(?P<workspace>\d+)/getCrossSellingProductTypes$', login_required(insightsapi.getCrossSellingProductTypes, login_url='/webapp/v1.0/login/'), name=u"apidata"),
    re_path(r'^(?P<workspace>\d+)/getCrossSellingProductTypes/(?P<account>.*)$', login_required(insightsapi.getCrossSellingProductTypes, login_url='/webapp/v1.0/login/'), name=u"apidata"),


    # Customers
    re_path(r'^(?P<workspace>\d+)/getdata$', login_required(customersapi.getCustomersData, login_url='/webapp/v1.0/login/'), name=u"apidata"),
    re_path(r'^(?P<workspace>\d+)/getcustomerslist$', login_required(customersapi.getCustomersList, login_url='/webapp/v1.0/login/'), name=u"apigetcustomerslist"),
    re_path(r'^(?P<workspace>\d+)/getcustomers$', login_required(customersapi.getCustomers, login_url='/webapp/v1.0/login/'), name=u"apigetcustomers"),
    re_path(r'^(?P<workspace>\d+)/getcustomers/(?P<account>.*)$', login_required(customersapi.getCustomers, login_url='/webapp/v1.0/login/'), name=u"apigetcustomers"),
    re_path(r'^(?P<workspace>\d+)/get_customers$', login_required(customersapi.get_customers, login_url='/webapp/v1.0/login/'), name=u"apigetcustomers"),
    re_path(r'^(?P<workspace>\d+)/get_customers/(?P<account>.*)$', login_required(customersapi.get_customers, login_url='/webapp/v1.0/login/'), name=u"apigetcustomers"),
    re_path(r'^(?P<workspace>\d+)/insertCustomer/(?P<data>.*)$', login_required(customersapi.insertCustomer), name=u"saveCustData"),
    re_path(r'^(?P<workspace>\d+)/modifyCustomer/(?P<data>.*)$', login_required(customersapi.modifyCustomer), name=u"saveCustData"),
    re_path(r'^(?P<workspace>\d+)/deleteCustomer/(?P<data>.*)$', login_required(customersapi.deleteCustomer), name=u"saveCustData"),

    # Contacts
    re_path(r'^(?P<workspace>\d+)/getdata$', login_required(contactsapi.getContactsData, login_url='/webapp/v1.0/login/'), name=u"apidata"),
    re_path(r'^(?P<workspace>\d+)/getcontactslist$', login_required(contactsapi.getContactsList, login_url='/webapp/v1.0/login/'), name=u"apigetcustomerslist"),
    re_path(r'^(?P<workspace>\d+)/getcontactslist/(?P<account>.*)$', login_required(contactsapi.getContactsList, login_url='/webapp/v1.0/login/'), name=u"apigetcustomerslist"),
    re_path(r'^(?P<workspace>\d+)/getcontacts$', login_required(contactsapi.getContacts, login_url='/webapp/v1.0/login/'), name=u"apigetcustomers"),
    re_path(r'^(?P<workspace>\d+)/getcontactsByCustomer$', login_required(contactsapi.getContactsByCustomer, login_url='/webapp/v1.0/login/'), name=u"apigetcustomers"),
    re_path(r'^(?P<workspace>\d+)/getcontactsByCustomer/(?P<account>.*)$', login_required(contactsapi.getContactsByCustomer, login_url='/webapp/login/'), name=u"apigetcustomers"),
    re_path(r'^(?P<workspace>\d+)/getcontacts/(?P<account>.*)$', login_required(contactsapi.getContacts, login_url='/webapp/login/'), name=u"apigetcustomers"),
    re_path(r'^(?P<workspace>\d+)/insertContact/(?P<data>.*)$', login_required(contactsapi.insertContact), name=u"saveCustData"),
    re_path(r'^(?P<workspace>\d+)/modifyContact/(?P<data>.*)$', login_required(contactsapi.modifyContact), name=u"saveCustData"),
    re_path(r'^(?P<workspace>\d+)/deleteContact/(?P<data>.*)$', login_required(contactsapi.deleteContact), name=u"saveCustData"),


    # # Sales
    re_path(r'^(?P<workspace>\d+)/insertSalesRecord/(?P<data>.*)$', login_required(salesapi.insertSalesRecord), name=u"saveCustData"),

    # # Products
    re_path(r'^(?P<workspace>\d+)/insertProduct/(?P<data>.*)$', login_required(productsapi.insertProduct), name=u"saveCustData"),
    re_path(r'^(?P<workspace>\d+)/insertProductType/(?P<data>.*)$', login_required(productsapi.insertProductType), name=u"saveCustData"),
    re_path(r'^(?P<workspace>\d+)/insertProductLine/(?P<data>.*)$', login_required(productsapi.insertProductLine), name=u"saveCustData"),
    re_path(r'^(?P<workspace>\d+)/insertProductClass/(?P<data>.*)$', login_required(productsapi.insertProductClass), name=u"saveCustData"),
    re_path(r'^(?P<workspace>\d+)/deleteProduct/(?P<product>.*)$', login_required(productsapi.deleteProduct), name=u"saveCustData"),
    re_path(r'^(?P<workspace>\d+)/deleteProductType/(?P<product>.*)$', login_required(productsapi.deleteProductType), name=u"saveCustData"),
    re_path(r'^(?P<workspace>\d+)/getProducts$', login_required(productsapi.getProducts), name=u"saveCustData"),
    re_path(r'^(?P<workspace>\d+)/getProductsBy$', login_required(productsapi.getProductsBy), name=u"saveCustData"),
    re_path(r'^(?P<workspace>\d+)/getProductsBy/(?P<groupby>.*)$', login_required(productsapi.getProductsBy), name=u"saveCustData"),
    re_path(r'^(?P<workspace>\d+)/getProductInsights$', login_required(productsapi.getProductInsights), name=u"saveCustData"),
    re_path(r'^(?P<workspace>\d+)/getProductInsights/(?P<params>.*)$', login_required(productsapi.getProductInsights), name=u"saveCustData"),
    re_path(r'^(?P<workspace>\d+)/get_product_insights$', login_required(productsapi.get_product_insights), name=u"saveCustData"),
    re_path(r'^(?P<workspace>\d+)/get_product_insights/(?P<params>.*)$', login_required(productsapi.get_product_insights), name=u"saveCustData"),
    re_path(r'^(?P<workspace>\d+)/getProductTypeInsights$', login_required(productsapi.getProductTypeInsights), name=u"saveCustData"),
    re_path(r'^(?P<workspace>\d+)/getProductTypeInsights/(?P<params>.*)$', login_required(productsapi.getProductTypeInsights), name=u"saveCustData"),
    re_path(r'^(?P<workspace>\d+)/topproducts$', login_required(productsapi.topProducts), name=u"setconfiginfo"),
    re_path(r'^(?P<workspace>\d+)/topproducts/(?P<params>.*)$', login_required(productsapi.topProducts), name=u"setconfiginfo"),

    # KAMs
    re_path(r'^(?P<workspace>\d+)/createKam/(?P<data>.*)$', login_required(actionsapi.createKam), name=u"saveCustData"),
    re_path(r'^(?P<workspace>\d+)/modifyKam/(?P<data>.*)$', login_required(actionsapi.modifyKam), name=u"saveCustData"),
    re_path(r'^(?P<workspace>\d+)/mergeKams/(?P<data>.*)$', login_required(actionsapi.mergeKams), name=u"saveCustData"),
    re_path(r'^(?P<workspace>\d+)/deleteKam/(?P<kamid>.*)$', login_required(actionsapi.deleteKam), name=u"saveCustData"),
    re_path(r'^(?P<workspace>\d+)/getKam/(?P<data>.*)$', login_required(actionsapi.getKam), name=u"saveCustData"),
    re_path(r'^(?P<workspace>\d+)/getKam$', login_required(actionsapi.getKam), name=u"saveCustData"),
    re_path(r'^(?P<workspace>\d+)/linkKamToAction/(?P<lk>.*)$', login_required(actionsapi.linkKamToAction), name=u"apigetplans"),
    re_path(r'^(?P<workspace>\d+)/unlinkKamFromAction/(?P<lk>.*)$', login_required(actionsapi.unlinkKamFromAction), name=u"apigetplans"),
    re_path(r'^(?P<workspace>\d+)/linkKamToPlan/(?P<lk>.*)$', login_required(actionsapi.linkKamToPlan), name=u"apigetplans"),
    re_path(r'^(?P<workspace>\d+)/unlinkKamFromPlan/(?P<lk>.*)$', login_required(actionsapi.unlinkKamFromPlan), name=u"apigetplans"),
    re_path(r'^(?P<workspace>\d+)/linkKamToCustomer/(?P<lk>.*)$', login_required(actionsapi.linkKamToCustomer), name=u"apigetplans"),
    re_path(r'^(?P<workspace>\d+)/unlinkKamFromCustomer/(?P<lk>.*)$', login_required(actionsapi.unlinkKamFromCustomer), name=u"apigetplans"),

    # Xing 
    # re_path(r'^(?P<workspace>\d+)/getXingJobs$', login_required(xingapi.getXingJobs), name=u"saveCustData"),
    # re_path(r'^(?P<workspace>\d+)/getXingUserProfile$', login_required(xingapi.getXingUserProfile), name=u"saveCustData"),

    # Goals
    re_path(r'^(?P<workspace>\d+)/createGoal/(?P<data>.*)$', login_required(goalsapi.createGoal), name=u"saveCustData"),
    re_path(r'^(?P<workspace>\d+)/modifyGoal/(?P<data>.*)$', login_required(goalsapi.modifyGoal), name=u"saveCustData"),
    re_path(r'^(?P<workspace>\d+)/getGoals/(?P<data>.*)$', login_required(goalsapi.getGoals), name=u"saveCustData"),
    re_path(r'^(?P<workspace>\d+)/getGoals$', login_required(goalsapi.getGoals), name=u"saveCustData"),
    re_path(r'^(?P<workspace>\d+)/getGoalsByYear/(?P<data>.*)$', login_required(goalsapi.getGoalsByYear), name=u"saveCustData"),
    re_path(r'^(?P<workspace>\d+)/getGoalsByYear$', login_required(goalsapi.getGoalsByYear), name=u"saveCustData"),
    re_path(r'^(?P<workspace>\d+)/getGoalsPerQuarter/(?P<data>.*)$', login_required(goalsapi.getGoalsPerQuarter), name=u"saveCustData"),
    re_path(r'^(?P<workspace>\d+)/getGoalsPerQuarter$', login_required(goalsapi.getGoalsPerQuarter), name=u"saveCustData"),
    #url(ur'^getGoals$', login_required(goalsapi.getGoals), name=u"saveCustData"),

    # Performance
    re_path(r'^(?P<workspace>\d+)/getTotalPerformance$', login_required(goalsapi.getTotalPerformance), name=u"saveCustData"),
    re_path(r'^(?P<workspace>\d+)/getPerformance$', login_required(goalsapi.getPerformance), name=u"saveCustData"),
    re_path(r'^(?P<workspace>\d+)/getPerformanceKpi$', login_required(goalsapi.getPerformanceKpi), name=u"saveCustData"),
    re_path(r'^(?P<workspace>\d+)/getPerformanceCRM$', login_required(goalsapi.getPerformanceCRM), name=u"saveCustData"),
    re_path(r'^(?P<workspace>\d+)/get_performance_crm$', login_required(goalsapi.get_performance_crm), name=u"saveCustData"),
    # re_path(r'^(?P<workspace>\d+)/get_performance_crm$', login_required(goalsapi.get_performance_crm), name=u"saveCustData"),
    
    # re_path(r'^(?P<workspace>\d+)/Performance_search$', login_required(goalsapi.get_performance_crm), name=u"saveCustData"),

    # Data analysis
    #url(ur'^(?P<workspace>\d+)/analyzeData$', login_required(dataanalysisapi.analyzeData), name=u"saveCustData"),

    # Actions
    re_path(r'^(?P<workspace>\d+)/getactions$', login_required(actionsapi.getTasks, login_url='/webapp/login/'), name=u"apigetactions"),
    re_path(r'^(?P<workspace>\d+)/getactions/(?P<account>.*)$', login_required(actionsapi.getTasks, login_url='/webapp/login/'), name=u"apigetactions"),
    re_path(r'^(?P<workspace>\d+)/getActions$', login_required(actionsapi.getActions, login_url='/webapp/login/'), name=u"apigetactions"),
    re_path(r'^(?P<workspace>\d+)/getActions/(?P<account>.*)$', login_required(actionsapi.getActions, login_url='/webapp/login/'), name=u"apigetactions"),
    re_path(r'^(?P<workspace>\d+)/createAction/(?P<task>.*)$', login_required(actionsapi.createAction), name=u"saveCustData"),
    re_path(r'^(?P<workspace>\d+)/setaction/(?P<task>.*)$', login_required(actionsapi.setTask), name=u"saveCustData"),
    re_path(r'^(?P<workspace>\d+)/deleteAction/(?P<task>.*)$', login_required(actionsapi.dropTask, login_url='/webapp/login/'), name=u"apidroptask"),
    re_path(r'^(?P<workspace>\d+)/modifyAction/(?P<action>.*)$', login_required(actionsapi.modifyAction), name=u"apicreateplan"),

    # Plans
    re_path(r'^(?P<workspace>\d+)/getplans$', login_required(actionsapi.getPlans), name=u"apigetplans"),
    re_path(r'^(?P<workspace>\d+)/getplans/(?P<account>.*)$', login_required(actionsapi.getPlans), name=u"apigetplans"),

    re_path(r'^(?P<workspace>\d+)/get_plans$', login_required(actionsapi.get_plans), name=u"apigetplans"),
    re_path(r'^(?P<workspace>\d+)/get_plans/(?P<account>.*)$', login_required(actionsapi.get_plans), name=u"apigetplans"),

    re_path(r'^(?P<workspace>\d+)/setplan/(?P<plan>.*)$', login_required(actionsapi.setPlan), name=u"apicreateplan"),
    re_path(r'^(?P<workspace>\d+)/createPlan/(?P<plan>.*)$', login_required(actionsapi.setPlan), name=u"apicreateplan"),
    re_path(r'^(?P<workspace>\d+)/modifyPlan/(?P<plan>.*)$', login_required(actionsapi.modifyPlan), name=u"apicreateplan"),
    re_path(r'^(?P<workspace>\d+)/deletePlan/(?P<planid>\d+)$', login_required(actionsapi.dropPlan), name=u"apidropplan"),

    # Plans and Actions
    re_path(r'^(?P<workspace>\d+)/plansToActions$', login_required(actionsapi.plansToActions), name=u"apigetplansperaciton"),
    re_path(r'^(?P<workspace>\d+)/getPlansPerAction$', login_required(actionsapi.getPlansGroupedByAction), name=u"apigetplansperaciton"),
    re_path(r'^(?P<workspace>\d+)/getPlansPerAction/(?P<account>.*)$', login_required(actionsapi.getPlansGroupedByAction), name=u"apigetplans"),
    re_path(r'^(?P<workspace>\d+)/getActionsPerPlan$', login_required(actionsapi.getActionsGroupedByPlan), name=u"apigetplans"),
    re_path(r'^(?P<workspace>\d+)/getActionsPerPlan/(?P<account>.*)$', login_required(actionsapi.getActionsGroupedByPlan), name=u"apigetplans"),
    re_path(r'^(?P<workspace>\d+)/linkPlanToAction/(?P<lk>.*)$', login_required(actionsapi.linkPlanToAction), name=u"apigetplans"),
    re_path(r'^(?P<workspace>\d+)/unlinkPlanFromAction/(?P<lk>.*)$', login_required(actionsapi.unlinkPlanFromAction), name=u"apigetplans"),

    # Users
    re_path(r'^(?P<workspace>\d+)/getuserprofile$', login_required(usersapi.getUserProfile, login_url='/webapp/login/'), name=u"getuserprofile"),
    re_path(r'^(?P<workspace>\d+)/getusertoken$', usersapi.getUserToken, name=u"getusertoken"),
    re_path(r'^(?P<workspace>\d+)/setContactInfo/(?P<info>.*)$', login_required(usersapi.setUserContactInfo, login_url='/webapp/login/'), name=u"setcontactinfo"),
    re_path(r'^(?P<workspace>\d+)/setactivityinfo/(?P<info>\w+)$', login_required(usersapi.setUserContactInfo, login_url='/webapp/login/'), name=u"setactivityinfo"),
    re_path(r'^(?P<workspace>\d+)/setconfiginfo/(?P<language>\w+)$', login_required(usersapi.setUserConfigInfo, login_url='/webapp/login/'), name=u"setconfiginfo"),

    # Groups 
    re_path(r'^(?P<workspace>\d+)/getGroups$', login_required(groupsapi.getGroups), name=u"apigetplans"),
    re_path(r'^(?P<workspace>\d+)/getGroups/(?P<user_id>[-\w\ ]+)$', login_required(groupsapi.getGroups), name=u"apigetplans"),
    re_path(r'^(?P<workspace>\d+)/createGroup/(?P<group>.*)$', login_required(groupsapi.createGroup), name=u"apicreateplan"),
    re_path(r'^(?P<workspace>\d+)/modifyGroup/(?P<group>.*)$', login_required(groupsapi.modifyGroup), name=u"apicreateplan"),
    re_path(r'^(?P<workspace>\d+)/deleteGroup/(?P<group_id>\d+)$', login_required(groupsapi.deleteGroup), name=u"apidropplan"),

    # Groups and Users
    re_path(r'^(?P<workspace>\d+)/getUsersPerGroup$', login_required(groupsapi.getUsersPerGroup), name=u"apigetplansperaciton"),
    re_path(r'^(?P<workspace>\d+)/getUsersPerGroup/(?P<user_name>[-\w\ ]+)$', login_required(groupsapi.getUsersPerGroup), name=u"apigetplans"),
    re_path(r'^(?P<workspace>\d+)/getGroupsPerUser$', login_required(groupsapi.getGroupsPerUser), name=u"apigetplansperaciton"),
    re_path(r'^(?P<workspace>\d+)/getGroupsPerUser/(?P<user_name>[-\w\ ]+)$', login_required(groupsapi.getGroupsPerUser), name=u"apigetplans"),
    re_path(r'^(?P<workspace>\d+)/addUserToGroup/(?P<lk>.*)$', login_required(groupsapi.addUserToGroup), name=u"apigetplans"),
    re_path(r'^(?P<workspace>\d+)/removeUserFromGroup/(?P<lk>.*)$', login_required(groupsapi.removeUserFromGroup), name=u"apigetplans"),

    # Maps
    re_path(r'^(?P<workspace>\d+)/maps/getCustomers$', login_required(mapsapi.getCustomers), name=u"setconfiginfo"),
    re_path(r'^(?P<workspace>\d+)/maps/getAllocation/(?P<details>.*)', login_required(mapsapi.getAllocation), name=u"setconfiginfo"),


    # --- Token access ---

    # Customers
    re_path(r'^(?P<user>\d+):(?P<token>[-\w\d-]+)/(?P<workspace>\d+)/getdata$', token_required(customersapi.getCustomersData), name=u"apidata"),
    re_path(r'^(?P<user>\d+):(?P<token>[-\w\d-]+)/(?P<workspace>\d+)/getdata/(?P<account>.*)$', token_required(customersapi.getCustomersData), name=u"apidata"),
    re_path(r'^(?P<user>\d+):(?P<token>[-\w\d-]+)/(?P<workspace>\d+)/getcustomers$', token_required(customersapi.getCustomers), name=u"apigetcustomers"),
    re_path(r'^(?P<user>\d+):(?P<token>[-\w\d-]+)/(?P<workspace>\d+)/getcustomers/(?P<account>.*)$', token_required(customersapi.getCustomers), name=u"apigetcustomers"),

    re_path(r'^(?P<user>\d+):(?P<token>[-\w\d-]+)/(?P<workspace>\d+)/get_customers$', token_required(customersapi.get_customers), name=u"apigetcustomers"),
    re_path(r'^(?P<user>\d+):(?P<token>[-\w\d-]+)/(?P<workspace>\d+)/get_customers/(?P<account>.*)$', token_required(customersapi.get_customers), name=u"apigetcustomers"),
    re_path(r'^(?P<user>\d+):(?P<token>[-\w\d-]+)/(?P<workspace>\d+)/get_group_customers$', token_required(customersapi.get_group_customers), name=u"apigetgroupcustomers"),

    re_path(r'^(?P<user>\d+):(?P<token>[-\w\d-]+)/(?P<workspace>\d+)/getcustomerslist$', token_required(customersapi.getCustomersList), name=u"apigetcustomerslist"),
    re_path(r'^(?P<user>\d+):(?P<token>[-\w\d-]+)/(?P<workspace>\d+)/insertCustomer/(?P<data>.*)$', token_required(customersapi.insertCustomer), name=u"saveCustData"),
    re_path(r'^(?P<user>\d+):(?P<token>[-\w\d-]+)/(?P<workspace>\d+)/modifyCustomer/(?P<data>.*)$', token_required(customersapi.modifyCustomer), name=u"saveCustData"),
    re_path(r'^(?P<user>\d+):(?P<token>[-\w\d-]+)/(?P<workspace>\d+)/deleteCustomer/(?P<data>.*)$', token_required(customersapi.deleteCustomer), name=u"saveCustData"),
    re_path(r'^(?P<user>\d+):(?P<token>[-\w\d-]+)/(?P<workspace>\d+)/getlinkedcustomers/(?P<account>.*)$', token_required(customersapi.getlinkedcustomers), name=u"apigetlinkedcustomers"),
    re_path(r'^(?P<user>\d+):(?P<token>[-\w\d-]+)/(?P<workspace>\d+)/getparentcustomers/(?P<account>.*)$', token_required(customersapi.getparentcustomers), name=u"apigetparentcustomers"),
    # re_path(r'^(?P<user>\d+):(?P<token>[-\w\d-]+)/(?P<workspace>\d+)/getparentcustomers/(?P<account>.*)$', token_required(customersapi.GetParentCustomers.as_view()), name=u"apigetparentcustomers"),
    re_path(r'^(?P<user>\d+):(?P<token>[-\w\d-]+)/(?P<workspace>\d+)/getSalesPerCustomer/(?P<account>.*)$', token_required(customersapi.get_sales_per_customer), name=u"getSalesPerCustomerapi"),
    re_path(r'^(?P<user>\d+):(?P<token>[-\w\d-]+)/(?P<workspace>\d+)/addLinkedCustomer/(?P<account>.*)$', token_required(customersapi.add_linked_customer), name=u"addLinkedCustomer"),
    re_path(r'^(?P<user>\d+):(?P<token>[-\w\d-]+)/(?P<workspace>\d+)/removeLinkedCustomer/(?P<account>.*)$', token_required(customersapi.remove_linked_customer), name=u"removeLinkedCustomer"),
    re_path(r'^(?P<user>\d+):(?P<token>[-\w\d-]+)/(?P<workspace>\d+)/getCustomerByProducts/(?P<account>.*)$', token_required(customersapi.customer_by_products), name=u"customerByProducts"),
    re_path(r'^(?P<user>\d+):(?P<token>[-\w\d-]+)/(?P<workspace>\d+)/getCustomerByProductTypes/(?P<account>.*)$', token_required(customersapi.customer_by_product_types), name=u"getCustomerByProductTypes"),

    # # Contacts
    re_path(r'^(?P<user>\d+):(?P<token>[-\w\d-]+)/(?P<workspace>\d+)/getdata$', token_required(contactsapi.getContactsData), name=u"apidata"),
    re_path(r'^(?P<user>\d+):(?P<token>[-\w\d-]+)/(?P<workspace>\d+)/getcontactslist$', token_required(contactsapi.getContactsList), name=u"apigetcustomerslist"),
    re_path(r'^(?P<user>\d+):(?P<token>[-\w\d-]+)/(?P<workspace>\d+)/getcontactslist/(?P<account>.*)$', token_required(contactsapi.getContactsList), name=u"apigetcustomerslist"),
    re_path(r'^(?P<user>\d+):(?P<token>[-\w\d-]+)/(?P<workspace>\d+)/getcontacts$', token_required(contactsapi.getContacts), name=u"apigetcustomers"),
    re_path(r'^(?P<user>\d+):(?P<token>[-\w\d-]+)/(?P<workspace>\d+)/getcontactsByCustomer$', token_required(contactsapi.getContactsByCustomer), name=u"apigetcustomers"),
    re_path(r'^(?P<user>\d+):(?P<token>[-\w\d-]+)/(?P<workspace>\d+)/getcontactsByCustomer/(?P<account>.*)$', token_required(contactsapi.getContactsByCustomer), name=u"apigetcustomers"),
    re_path(r'^(?P<user>\d+):(?P<token>[-\w\d-]+)/(?P<workspace>\d+)/getcontacts/(?P<account>.*)$', token_required(contactsapi.getContacts), name=u"apigetcustomers"),
    re_path(r'^(?P<user>\d+):(?P<token>[-\w\d-]+)/(?P<workspace>\d+)/insertContact/(?P<data>.*)$', token_required(contactsapi.insertContact), name=u"saveCustData"),
    re_path(r'^(?P<user>\d+):(?P<token>[-\w\d-]+)/(?P<workspace>\d+)/modifyContact/(?P<data>.*)$', token_required(contactsapi.modifyContact), name=u"saveCustData"),
    re_path(r'^(?P<user>\d+):(?P<token>[-\w\d-]+)/(?P<workspace>\d+)/deleteContact/(?P<data>.*)$', token_required(contactsapi.deleteContact), name=u"saveCustData"),

    # # Sales
    re_path(r'^(?P<user>\d+):(?P<token>[-\w\d-]+)/(?P<workspace>\d+)/insertSalesRecord/(?P<data>.*)$', token_required(salesapi.insertSalesRecord), name=u"saveCustData"),

    # KAMs
    re_path(r'^(?P<user>\d+):(?P<token>[-\w\d-]+)/(?P<workspace>\d+)/createKam/(?P<data>.*)$', token_required(actionsapi.createKam), name=u"saveCustData"),
    re_path(r'^(?P<user>\d+):(?P<token>[-\w\d-]+)/(?P<workspace>\d+)/modifyKam/(?P<data>.*)$', token_required(actionsapi.modifyKam), name=u"saveCustData"),
    re_path(r'^(?P<user>\d+):(?P<token>[-\w\d-]+)/(?P<workspace>\d+)/mergeKams/(?P<data>.*)$', token_required(actionsapi.mergeKams), name=u"saveCustData"),
    re_path(r'^(?P<user>\d+):(?P<token>[-\w\d-]+)/(?P<workspace>\d+)/deleteKam/(?P<kamid>.*)$', token_required(actionsapi.deleteKam), name=u"saveCustData"),
    re_path(r'^(?P<user>\d+):(?P<token>[-\w\d-]+)/(?P<workspace>\d+)/getKam$', token_required(actionsapi.getKam), name=u"saveCustData"),
    re_path(r'^(?P<user>\d+):(?P<token>[-\w\d-]+)/(?P<workspace>\d+)/getKam/(?P<data>.*)$', token_required(actionsapi.getKam), name=u"saveCustData"),
    re_path(r'^(?P<user>\d+):(?P<token>[-\w\d-]+)/(?P<workspace>\d+)/linkKamToAction/(?P<lk>.*)$', token_required(actionsapi.linkKamToAction), name=u"apigetplans"),
    re_path(r'^(?P<user>\d+):(?P<token>[-\w\d-]+)/(?P<workspace>\d+)/unlinkKamFromAction/(?P<lk>.*)$', token_required(actionsapi.unlinkKamFromAction), name=u"apigetplans"),
    re_path(r'^(?P<user>\d+):(?P<token>[-\w\d-]+)/(?P<workspace>\d+)/linkKamToPlan/(?P<lk>.*)$', token_required(actionsapi.linkKamToPlan), name=u"apigetplans"),
    re_path(r'^(?P<user>\d+):(?P<token>[-\w\d-]+)/(?P<workspace>\d+)/unlinkKamFromPlan/(?P<lk>.*)$', token_required(actionsapi.unlinkKamFromPlan), name=u"apigetplans"),
    re_path(r'^(?P<user>\d+):(?P<token>[-\w\d-]+)/(?P<workspace>\d+)/linkKamToCustomer/(?P<lk>.*)$', token_required(actionsapi.linkKamToCustomer), name=u"apigetplans"),
    re_path(r'^(?P<user>\d+):(?P<token>[-\w\d-]+)/(?P<workspace>\d+)/unlinkKamFromCustomer/(?P<lk>.*)$', token_required(actionsapi.unlinkKamFromCustomer), name=u"apigetplans"),

    # Xing 
    # re_path(r'^(?P<user>\d+):(?P<token>[-\w\d-]+)/(?P<workspace>\d+)/getXingJobs$', token_required(xingapi.getXingJobs), name=u"saveCustData"),
    # re_path(r'^(?P<user>\d+):(?P<token>[-\w\d-]+)/(?P<workspace>\d+)/getXingUserProfile$', token_required(xingapi.getXingUserProfile), name=u"saveCustData"),

    # Goals
    re_path(r'^(?P<user>\d+):(?P<token>[-\w\d-]+)/(?P<workspace>\d+)/createGoal/(?P<data>.*)$', token_required(goalsapi.createGoal), name=u"saveCustData"),
    re_path(r'^(?P<user>\d+):(?P<token>[-\w\d-]+)/(?P<workspace>\d+)/modifyGoal/(?P<data>.*)$', token_required(goalsapi.modifyGoal), name=u"saveCustData"),
    re_path(r'^(?P<user>\d+):(?P<token>[-\w\d-]+)/(?P<workspace>\d+)/getGoals/(?P<data>.*)$', token_required(goalsapi.getGoals), name=u"saveCustData"),
    re_path(r'^(?P<user>\d+):(?P<token>[-\w\d-]+)/(?P<workspace>\d+)/getGoals$', token_required(goalsapi.getGoals), name=u"saveCustData"),
    re_path(r'^(?P<user>\d+):(?P<token>[-\w\d-]+)/(?P<workspace>\d+)/getGoalsByYear/(?P<data>.*)$', token_required(goalsapi.getGoalsByYear), name=u"saveCustData"),
    re_path(r'^(?P<user>\d+):(?P<token>[-\w\d-]+)/(?P<workspace>\d+)/getGoalsByYear$', token_required(goalsapi.getGoalsByYear), name=u"saveCustData"),
    re_path(r'^(?P<user>\d+):(?P<token>[-\w\d-]+)/(?P<workspace>\d+)/getGoalsPerQuarter/(?P<data>.*)$', token_required(goalsapi.getGoalsPerQuarter), name=u"saveCustData"),
    re_path(r'^(?P<user>\d+):(?P<token>[-\w\d-]+)/(?P<workspace>\d+)/getGoalsPerQuarter$', token_required(goalsapi.getGoalsPerQuarter), name=u"saveCustData"),


    # Performance
    re_path(r'^(?P<user>\d+):(?P<token>[-\w\d-]+)/(?P<workspace>\d+)/getTotalPerformance$', token_required(goalsapi.getTotalPerformance), name=u"saveCustData"),
    re_path(r'^(?P<user>\d+):(?P<token>[-\w\d-]+)/(?P<workspace>\d+)/getPerformance$', token_required(goalsapi.getPerformance), name=u"saveCustData"),
    re_path(r'^(?P<user>\d+):(?P<token>[-\w\d-]+)/(?P<workspace>\d+)/getPerformanceKpi$', token_required(goalsapi.getPerformanceKpi), name=u"saveCustData"),
    re_path(r'^(?P<user>\d+):(?P<token>[-\w\d-]+)/(?P<workspace>\d+)/getPerformanceCRM$', token_required(goalsapi.getPerformanceCRM), name=u"saveCustData"),
    re_path(r'^(?P<user>\d+):(?P<token>[-\w\d-]+)/(?P<workspace>\d+)/get_performance_crm$', token_required(goalsapi.get_performance_crm), name=u"saveCustData"),
    re_path(r'^(?P<user>\d+):(?P<token>[-\w\d-]+)/(?P<workspace>\d+)/get_performance_products$', token_required(goalsapi.get_performance_products), name=u"PerformanceProduct"),
    re_path(r'^(?P<user>\d+):(?P<token>[-\w\d-]+)/(?P<workspace>\d+)/performance_search/(?P<data>.*)$', token_required(goalsapi.performance_search), name=u"search"),

    re_path(r'^(?P<user>\d+):(?P<token>[-\w\d-]+)/(?P<workspace>\d+)/get_sales_year/$', token_required(goalsapi.get_sales_year), name=u"getSalesYear"),

    # reports
    re_path(r'^(?P<user>\d+):(?P<token>[-\w\d-]+)/(?P<workspace>\d+)/insertReport/(?P<data>.*)$', token_required(goalsapi.insertReport), name=u"insertreport"),
    re_path(r'^(?P<user>\d+):(?P<token>[-\w\d-]+)/(?P<workspace>\d+)/getReport/(?P<data>.*)$', token_required(goalsapi.getReport), name=u"getreport"),
    re_path(r'^(?P<user>\d+):(?P<token>[-\w\d-]+)/(?P<workspace>\d+)/modifyReport/(?P<data>.*)$', token_required(goalsapi.modifyReport), name=u"modifyreport"),
    re_path(r'^(?P<user>\d+):(?P<token>[-\w\d-]+)/(?P<workspace>\d+)/deleteReport/(?P<data>.*)$', token_required(goalsapi.dropReport), name=u"dropreport"),

    # Data analysis
    re_path(r'^(?P<user>\d+):(?P<token>[-\w\d-]+)/(?P<workspace>\d+)/analyzeData$', token_required(dataanalysisapi.analyzeData), name=u"saveCustData"),

    # Insights
    re_path(r'^(?P<user>\d+):(?P<token>[-\w\d-]+)/(?P<workspace>\d+)/getallinsights$', token_required(insightsapi.getAllInsights), name=u"getinsights"),
    re_path(r'^(?P<user>\d+):(?P<token>[-\w\d-]+)/(?P<workspace>\d+)/getallinsights/(?P<account>.*)$', token_required(insightsapi.getAllInsights), name=u"getinsights"),
    re_path(r'^(?P<user>\d+):(?P<token>[-\w\d-]+)/(?P<workspace>\d+)/getinsights$', token_required(insightsapi.getInsights), name=u"getinsights"),
    re_path(r'^(?P<user>\d+):(?P<token>[-\w\d-]+)/(?P<workspace>\d+)/getinsights/(?P<account>.*)$', token_required(insightsapi.getInsights), name=u"getinsights"),
    re_path(r'^(?P<user>\d+):(?P<token>[-\w\d-]+)/(?P<workspace>\d+)/get_insights$', token_required(insightsapi.get_insights), name=u"apidata"),
    re_path(r'^(?P<user>\d+):(?P<token>[-\w\d-]+)/(?P<workspace>\d+)/get_insights/(?P<account>.*)$', token_required(insightsapi.get_insights), name=u"apidata"),
    re_path(r'^(?P<user>\d+):(?P<token>[-\w\d-]+)/(?P<workspace>\d+)/getCustomerRisk$', token_required(insightsapi.getCustomerRisk), name=u"apidata"),
    re_path(r'^(?P<user>\d+):(?P<token>[-\w\d-]+)/(?P<workspace>\d+)/getCustomerRisk/(?P<account>[-\w ]+)$', token_required(insightsapi.getCustomerRisk), name=u"apidata"),
    re_path(r'^(?P<user>\d+):(?P<token>[-\w\d-]+)/(?P<workspace>\d+)/getProductRisk$', token_required(insightsapi.getProductRisk), name=u"apidata"),
    re_path(r'^(?P<user>\d+):(?P<token>[-\w\d-]+)/(?P<workspace>\d+)/getProductRisk/(?P<account>[-\w ]+)$', token_required(insightsapi.getProductRisk), name=u"apidata"),
    re_path(r'^(?P<user>\d+):(?P<token>[-\w\d-]+)/(?P<workspace>\d+)/getProductTypeRisk$', token_required(insightsapi.getProductTypeRisk), name=u"apidata"),
    re_path(r'^(?P<user>\d+):(?P<token>[-\w\d-]+)/(?P<workspace>\d+)/getProductTypeRisk/(?P<account>[-\w ]+)$', token_required(insightsapi.getProductTypeRisk), name=u"apidata"),

    # Actions
    re_path(r'^(?P<user>\d+):(?P<token>[-\w\d-]+)/(?P<workspace>\d+)/setaction/(?P<task>.*)$', token_required(actionsapi.setTask), name=u"saveCustData"),
    re_path(r'^(?P<user>\d+):(?P<token>[-\w\d-]+)/(?P<workspace>\d+)/createAction/(?P<task>.*)$', token_required(actionsapi.createAction), name=u"saveCustData"),
    re_path(r'^(?P<user>\d+):(?P<token>[-\w\d-]+)/(?P<workspace>\d+)/deleteAction/(?P<task>.*)$', token_required(actionsapi.dropTask), name=u"apidroptask"),
    re_path(r'^(?P<user>\d+):(?P<token>[-\w\d-]+)/(?P<workspace>\d+)/modifyAction/(?P<action>.*)$', token_required(actionsapi.modifyAction), name=u"apicreateplan"),
    re_path(r'^(?P<user>\d+):(?P<token>[-\w\d-]+)/(?P<workspace>\d+)/getactions$', token_required(actionsapi.getTasks), name=u"apigetactions"),
    re_path(r'^(?P<user>\d+):(?P<token>[-\w\d-]+)/(?P<workspace>\d+)/getactions/(?P<account>.*)$', token_required(actionsapi.getTasks), name=u"apigetactions"),
    re_path(r'^(?P<user>\d+):(?P<token>[-\w\d-]+)/(?P<workspace>\d+)/getActions$', token_required(actionsapi.getActions), name=u"apigetactions"),
    re_path(r'^(?P<user>\d+):(?P<token>[-\w\d-]+)/(?P<workspace>\d+)/getActions/(?P<account>.*)$', token_required(actionsapi.getActions), name=u"apigetactions"),

    # Plans
    re_path(r'^(?P<user>\d+):(?P<token>[-\w\d-]+)/(?P<workspace>\d+)/setplan/(?P<plan>.*)$', token_required(actionsapi.setPlan), name=u"apicreateplan"),
    re_path(r'^(?P<user>\d+):(?P<token>[-\w\d-]+)/(?P<workspace>\d+)/modifyPlan/(?P<plan>.*)$', token_required(actionsapi.modifyPlan), name=u"apicreateplan"),
    re_path(r'^(?P<user>\d+):(?P<token>[-\w\d-]+)/(?P<workspace>\d+)/deletePlan/(?P<planid>\d+)$', token_required(actionsapi.dropPlan), name=u"apidropplan"),
    re_path(r'^(?P<user>\d+):(?P<token>[-\w\d-]+)/(?P<workspace>\d+)/getplans$', token_required(actionsapi.getPlans), name=u"apigetplans"),
    re_path(r'^(?P<user>\d+):(?P<token>[-\w\d-]+)/(?P<workspace>\d+)/getplans/(?P<account>.*)$', token_required(actionsapi.getPlans), name=u"apigetplans"),

    re_path(r'^(?P<user>\d+):(?P<token>[-\w\d-]+)/(?P<workspace>\d+)/get_plans$', token_required(actionsapi.get_plans), name=u"apigetplans"),
    re_path(r'^(?P<user>\d+):(?P<token>[-\w\d-]+)/(?P<workspace>\d+)/get_plans/(?P<account>.*)$', token_required(actionsapi.get_plans), name=u"apigetplans"),

    # Plans and Actions
    re_path(r'^(?P<user>\d+):(?P<token>[-\w\d-]+)/(?P<workspace>\d+)/plansToActions$', token_required(actionsapi.plansToActions), name=u"apigetplansperaciton"),
    re_path(r'^(?P<user>\d+):(?P<token>[-\w\d-]+)/(?P<workspace>\d+)/getPlansPerAction$', token_required(actionsapi.getPlansGroupedByAction), name=u"apigetplansperaciton"),
    re_path(r'^(?P<user>\d+):(?P<token>[-\w\d-]+)/(?P<workspace>\d+)/getPlansPerAction/(?P<account>.*)$', token_required(actionsapi.getPlansGroupedByAction), name=u"apigetplans"),
    re_path(r'^(?P<user>\d+):(?P<token>[-\w\d-]+)/(?P<workspace>\d+)/getActionsPerPlan$', token_required(actionsapi.getActionsGroupedByPlan), name=u"apigetplans"),
    re_path(r'^(?P<user>\d+):(?P<token>[-\w\d-]+)/(?P<workspace>\d+)/getActionsPerPlan/(?P<account>.*)$', token_required(actionsapi.getActionsGroupedByPlan), name=u"apigetplans"),
    re_path(r'^(?P<user>\d+):(?P<token>[-\w\d-]+)/(?P<workspace>\d+)/linkPlanToAction/(?P<lk>.*)$', token_required(actionsapi.linkPlanToAction), name=u"apigetplans"),
    re_path(r'^(?P<user>\d+):(?P<token>[-\w\d-]+)/(?P<workspace>\d+)/unlinkPlanFromAction/(?P<lk>.*)$', token_required(actionsapi.unlinkPlanFromAction), name=u"apigetplans"),


    # Users
    re_path(r'^(?P<user>\d+):(?P<token>[-\w\d-]+)/(?P<workspace>\d+)/getuserprofile$', token_required(usersapi.getUserProfile), name=u"getuserprofile"),
    re_path(r'^(?P<token>[-\w\d-]+)/(?P<workspace>\d+)/getuserprofile$', token_required(usersapi.getUserProfile), name=u"getuserprofile"),
    re_path(r'^(?P<user>\d+):(?P<token>[-\w\d-]+)/(?P<workspace>\d+)/setContactInfo/(?P<info>.*)$', token_required(usersapi.setUserContactInfo), name=u"setcontactinfo"),
    re_path(r'^(?P<user>\d+):(?P<token>[-\w\d-]+)/(?P<workspace>\d+)/setactivityinfo/(?P<lastUpload>\w+)/(?P<lastFileUploaded>\w+)$', token_required(usersapi.setUserContactInfo), name=u"setactivityinfo"),
    re_path(r'^(?P<user>\d+):(?P<token>[-\w\d-]+)/(?P<workspace>\d+)/setconfiginfo/(?P<language>\w+)$', token_required(usersapi.setUserConfigInfo), name=u"setconfiginfo"),
    re_path(r'^(?P<user>\d+):(?P<token>[-\w\d-]+)/(?P<workspace>\d+)/setavatarimages$', token_required(usersapi.setavatarImages), name=u"setavatarimages"),
    re_path(r'^(?P<user>\d+):(?P<token>[-\w\d-]+)/(?P<workspace>\d+)/change_password/(?P<password_info>.*)$', token_required(usersapi.change_password), name=u"change_password"),

    # Groups 
    re_path(r'^(?P<user>\d+):(?P<token>[-\w\d-]+)/(?P<workspace>\d+)/getGroups$', token_required(groupsapi.getGroups), name=u"apigetplans"),
    re_path(r'^(?P<user>\d+):(?P<token>[-\w\d-]+)/(?P<workspace>\d+)/getGroups/(?P<user_id>[-\w\ ]+)$', token_required(groupsapi.getGroups), name=u"apigetplans"),
    re_path(r'^(?P<user>\d+):(?P<token>[-\w\d-]+)/(?P<workspace>\d+)/createGroup/(?P<group>.*)$', token_required(groupsapi.createGroup), name=u"apicreateplan"),
    re_path(r'^(?P<user>\d+):(?P<token>[-\w\d-]+)/(?P<workspace>\d+)/modifyGroup/(?P<group>.*)$', token_required(groupsapi.modifyGroup), name=u"apicreateplan"),
    re_path(r'^(?P<user>\d+):(?P<token>[-\w\d-]+)/(?P<workspace>\d+)/deleteGroup/(?P<group_id>\d+)$', token_required(groupsapi.deleteGroup), name=u"apidropplan"),

    # Groups and Users
    re_path(r'^(?P<user>\d+):(?P<token>[-\w\d-]+)/(?P<workspace>\d+)/getUsersPerGroup$', token_required(groupsapi.getUsersPerGroup), name=u"apigetplansperaciton"),
    re_path(r'^(?P<user>\d+):(?P<token>[-\w\d-]+)/(?P<workspace>\d+)/getUsersPerGroup/(?P<user_name>[-\w\ ]+)$', token_required(groupsapi.getUsersPerGroup), name=u"apigetplans"),
    re_path(r'^(?P<user>\d+):(?P<token>[-\w\d-]+)/(?P<workspace>\d+)/getGroupsPerUser$', token_required(groupsapi.getGroupsPerUser), name=u"apigetplansperaciton"),
    re_path(r'^(?P<user>\d+):(?P<token>[-\w\d-]+)/(?P<workspace>\d+)/getGroupsPerUser/(?P<user_name>[-\w\ ]+)$', token_required(groupsapi.getGroupsPerUser), name=u"apigetplans"),
    re_path(r'^(?P<user>\d+):(?P<token>[-\w\d-]+)/(?P<workspace>\d+)/addUserToGroup/(?P<lk>.*)$', token_required(groupsapi.addUserToGroup), name=u"apigetplans"),
    re_path(r'^(?P<user>\d+):(?P<token>[-\w\d-]+)/(?P<workspace>\d+)/removeUserFromGroup/(?P<lk>.*)$', token_required(groupsapi.removeUserFromGroup), name=u"apigetplans"),

    # Maps
    re_path(r'^(?P<user>\d+):(?P<token>[-\w\d-]+)/(?P<workspace>\d+)/maps/getCustomersData$', token_required(mapsapi.getCustomers), name=u"setconfiginfo"),
    re_path(r'^(?P<user>\d+):(?P<token>[-\w\d-]+)/(?P<workspace>\d+)/maps/getAllocation/(?P<details>.*)', token_required(mapsapi.getAllocation), name=u"setconfiginfo"),

    # Products
    re_path(r'^(?P<user>\d+):(?P<token>[-\w\d-]+)/(?P<workspace>\d+)/insertProduct/(?P<data>.*)$', token_required(productsapi.insertProduct), name=u"saveCustData"),
    re_path(r'^(?P<user>\d+):(?P<token>[-\w\d-]+)/(?P<workspace>\d+)/insertProductType/(?P<data>.*)$', token_required(productsapi.insertProductType), name=u"saveCustData"),
    re_path(r'^(?P<user>\d+):(?P<token>[-\w\d-]+)/(?P<workspace>\d+)/insertProductLine/(?P<data>.*)$', token_required(productsapi.insertProductLine), name=u"saveCustData"),
    re_path(r'^(?P<user>\d+):(?P<token>[-\w\d-]+)/(?P<workspace>\d+)/insertProductClass/(?P<data>.*)$', token_required(productsapi.insertProductClass), name=u"saveCustData"),
    re_path(r'^(?P<user>\d+):(?P<token>[-\w\d-]+)/(?P<workspace>\d+)/deleteProduct/(?P<product>.*)$', token_required(productsapi.deleteProduct), name=u"saveCustData"),
    re_path(r'^(?P<user>\d+):(?P<token>[-\w\d-]+)/(?P<workspace>\d+)/deleteProductType/(?P<product>.*)$', token_required(productsapi.deleteProductType), name=u"saveCustData"),
    re_path(r'^(?P<user>\d+):(?P<token>[-\w\d-]+)/(?P<workspace>\d+)/getProducts$', token_required(productsapi.getProducts), name=u"saveCustData"),
    re_path(r'^(?P<user>\d+):(?P<token>[-\w\d-]+)/(?P<workspace>\d+)/getProducts/(?P<product>.*)$', token_required(productsapi.getProducts), name=u"saveCustData"),
    re_path(r'^(?P<user>\d+):(?P<token>[-\w\d-]+)/(?P<workspace>\d+)/getProductsBy$', token_required(productsapi.getProductsBy), name=u"saveCustData"),
    re_path(r'^(?P<user>\d+):(?P<token>[-\w\d-]+)/(?P<workspace>\d+)/getProductsBy/(?P<groupby>.*)$', token_required(productsapi.getProductsBy), name=u"saveCustData"),
    re_path(r'^(?P<user>\d+):(?P<token>[-\w\d-]+)/(?P<workspace>\d+)/getProductsByType/(?P<data>.*)$', token_required(productsapi.getProductsByType), name=u"product_by_type"),
    re_path(r'^(?P<user>\d+):(?P<token>[-\w\d-]+)/(?P<workspace>\d+)/getProductsByCustomer/(?P<data>.*)$', token_required(productsapi.getProductsByCustomer), name=u"product_by_customer"),
    re_path(r'^(?P<user>\d+):(?P<token>[-\w\d-]+)/(?P<workspace>\d+)/getMinMaxVal/(?P<data>.*)$', token_required(productsapi.getMinMaxVal), name=u"ge_tMin_Max_Val"),

    re_path(r'^(?P<user>\d+):(?P<token>[-\w\d-]+)/(?P<workspace>\d+)/getProductsByCustomer/(?P<data>.*)$', token_required(productsapi.getProductsByCustomer), name=u"product_by_customer"),
    re_path(r'^(?P<user>\d+):(?P<token>[-\w\d-]+)/(?P<workspace>\d+)/getMinMaxVal/(?P<data>.*)$', token_required(productsapi.getMinMaxVal), name=u"get_tMin_Max_Val"),
    re_path(r'^(?P<user>\d+):(?P<token>[-\w\d-]+)/(?P<workspace>\d+)/getsuggestedRange/(?P<data>.*)$', token_required(productsapi.getSuggestedRange), name=u"get_suggested_range"),

    re_path(r'^(?P<user>\d+):(?P<token>[-\w\d-]+)/(?P<workspace>\d+)/getProductInsights$', token_required(productsapi.getProductInsights), name=u"saveCustData"),
    re_path(r'^(?P<user>\d+):(?P<token>[-\w\d-]+)/(?P<workspace>\d+)/getProductInsights/(?P<params>.*)$', token_required(productsapi.getProductInsights), name=u"saveCustData"),

    re_path(r'^(?P<user>\d+):(?P<token>[-\w\d-]+)/(?P<workspace>\d+)/get_product_insights$', token_required(productsapi.get_product_insights), name=u"saveCustData"),
    re_path(r'^(?P<user>\d+):(?P<token>[-\w\d-]+)/(?P<workspace>\d+)/get_product_insights/(?P<params>.*)$', token_required(productsapi.get_product_insights), name=u"saveCustData"),

    re_path(r'^(?P<user>\d+):(?P<token>[-\w\d-]+)/(?P<workspace>\d+)/getProductTypeInsights$', token_required(productsapi.getProductTypeInsights), name=u"saveCustData"),
    re_path(r'^(?P<user>\d+):(?P<token>[-\w\d-]+)/(?P<workspace>\d+)/getProductTypeInsights/(?P<params>.*)$', token_required(productsapi.getProductTypeInsights), name=u"saveCustData"),

    re_path(r'^(?P<user>\d+):(?P<token>[-\w\d-]+)/(?P<workspace>\d+)/topproducts$', token_required(productsapi.topProducts), name=u"setconfiginfo"),
    re_path(r'^(?P<user>\d+):(?P<token>[-\w\d-]+)/(?P<workspace>\d+)/topproducts/(?P<params>.*)$', token_required(productsapi.topProducts), name=u"setconfiginfo"),

    # industry
    re_path(r'^(?P<user>\d+):(?P<token>[-\w\d-]+)/(?P<workspace>\d+)/get_industries$', token_required(industryapi.get_industry), name=u"getIndustry"),

    # Pricing
    # re_path(r'^(?P<user>\d+):(?P<token>[-\w\d-]+)/(\d+)/product-price-suggestion$', token_required(product_price_suggestion.suggest_price_for_product), name=u"suggest_price"),
]