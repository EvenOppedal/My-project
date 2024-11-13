library(pickmdl)
# Henter data fra statistikkbanken

VHI <- select(as_tibble(ApiData("https://data.ssb.no/api/v0/no/table/07129/",ContentsCode ="VolumUjustert",Tid=TRUE,NACE=TRUE)$dataset),-ContentsCode,-NAstatus)
VHI <- mutate(VHI,NACE=paste0(paste0("SNN",NACE),"_IVL_U"))

VHI <- pivot_wider(VHI,names_from=NACE,values_from=value)


## Velger ut Varehandelsindeksen for dagligvarehandel. Gjøre om til tidsserie-objekt

VHI_471 <- as.numeric(VHI$SNN47.1_IVL_U)
VHI_471 <- ts(VHI_471,start=c(2000,1),frequency=12)

# sesongjustering med spefikasjon RSA5c 

# Det er ikke nødvendig å laste inn et datasett for å hente ut en spec
model_rsa5c <- x13(VHI_471,spec = "RSA5c")

# se nærmere på resultatet:

model_rsa5c$regarima      # detaljer om forhåndsjustering
model_rsa5c$final$series  # komponentene
model_rsa5c$decomposition # informasjon om filterlengder 
model_rsa5c$diagnostics   # tester for residualsesong 

rsa5c_spec <- x13_spec(model_rsa5c)
rsa5c_additiv <- x13_spec(rsa5c_spec, transform.function = "None")
model_rsa5c_add <- x13(VHI_471,rsa5c_additiv)


# sette working / trading days
# Her kan man altså sette inn Spec direkte som første arg
rsa5c_wd <- x13_spec(spec = "RSA5c", tradingdays.option = "WorkingDays")
# Disse to er avhengig av at man først har definert rsa5c_spec i linjene over. I stedet for rsa5c_spec kan man bare skrive "RSA5c"
rsa5c_td <- x13_spec(rsa5c_spec, tradingdays.option = "TradingDays")
rsa5c_notd <- x13_spec(rsa5c_spec, tradingdays.option = "None")

rsa5c_outliers <- x13_spec(rsa5c_spec, usrdef.outliersEnabled = TRUE, usrdef.outliersType = c("LS", "AO"), usrdef.outliersDate = c("2020-03-01", "2019-04-01"))

kalender_1 <- konstruksjon(forste_ar = 2000, siste_ar = 2050, 
                           k_roddag = TRUE, t_roddag = "sondag", 
                           rod_dag = c("jan1", "mai1", "mai17", "des24", "des25", "des26"), 
                           k_fpk = TRUE, ant_fpk = 7, t_fpk = "egen_effekt", 
                           paske_egen = 1, paske_mdl = "X12", t_pklordag = "egen_effekt",
                           t_pinse = "sondag", k_td = TRUE, td_type = "TD6", 
                           k_grupper = TRUE, monster = c(1, 1, 2, 2, 2, 3), 
                           fjerne_se_td = TRUE, skudd_ar = TRUE)$samle_mnd[,-1]
kalender2 <- ts(kalender_1, start = c(2000, 1), frequency=12)

### sesongjustere med egendefinert kalender       

kalender1_spec <- x13_spec("RSA5c",usrdef.varEnabled= TRUE, usrdef.varType = "Calendar",usrdef.var=kalender2)

model_kalender1 <- x13(VHI_471,kalender1_spec)


# ulike typer innebygde plot 

plot(model_rsa5c,type_chart="sa-trend")