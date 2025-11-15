-- Decode first route polyline into a LineString (EPSG:4326)
SELECT
  ST_LineFromEncodedPolyline(
    'xqjfFe}wtZf@oJ{BWiD_@sD_@}TcCyDa@iBM{DUwLoAWBQA_E]}AUuAKWBQBUL[ZMVIXSz@K^e@tB]dBUvAq@zFM~ASPEn@MlBWnEU|DChAKhBc@zEo@hEYzAa@nBi@vB}A~EO^oChGoA|BsCxFm@tA{@|BoAzDo@fCe@xB_@rBg@`DYxBWlC}@hLcAdM_AdK_@rEkBlUe@tES`B[vBaAhFeAbEgAtDk@`ByArDkAhCu@tAsC|EaDvFc@z@_F`K{BbFcC|FiAtC}A|Ea@fBStAYvCEtB?tBLpEv@zRDjFIpBM`B[bCSt@e@pBe@zAm@xAkA|B{AtBm@p@gAbAaAv@uAx@_Bt@YNo@RsBp@gBh@oGvBa@PmB~@cAn@mBtA_DpCeDxCiA|@_BbAcCdA}@ZaDp@_a@zH{JpBcBZyA`@aCz@sAn@iBlAmC~BaBnBk@v@_AdBWj@c@fAs@`CiAzE}@fD_@jA_A|BiBdD_BlCsBbEk@rA}@fCc@zAk@rCq@`FQtA[fCOn@k@pCk@lBaAxBu@tA}@pAiAlAaBrAi@^k@Zg@TeBn@oB^kBNmB@oDMwBEeA@qAHoBZiAZgBv@kAv@s@j@}@`Ay@`As@nAa@z@_@hAk@jBe@|BW|BKfBCvBHzCNlBfAnIHfB@zAEtAI~@UxAYnAWz@e@lAe@z@k@t@u@x@uAnA{DbDcEfD{G|FoAjA}@hAu@rAa@`ASp@]|AWfBgAxJcAvI_AhHYtCKjBAvADpBHnAPtA^|ArArEt@vDH|@DlAAlCg@vGYpDEtA@jAJlB`@vBh@~AHTf@bA|BvDfArB\\n@Xr@j@zAh@dBx@vDl@|CVzAFl@HpBAhBMdB[lBaAzEk@xCQrAy@lFa@nAg@fAw@pA{@dAeBlBuAvAeEbEqBfBkDfCaBhA}AxAY\\cA`Ba@`Am@nBQz@g@|Ce@`EW|CMnCQbFOnEK`DYvF_AbKe@fFOfDAbDJxDXfDNrA^rBfBfIt@lDLDDJf@pB^~A`A`Ez@rD`@rCLnBD`@P`AZ|AaCvByFpFkBlBsBzB}@|@}@l@aAb@{@Vc@FoEXkBLwAN{@TsEbBeIrCaExAmDnA}HnCcBn@Os@SiAe@cCe@wBU{AgCiMoAuG[qAq@yDKe@l@UpBq@~B}@'
  )::geometry(LineString, 4326) AS route_geom;

-- Persist second route polyline into a table route_m1
DROP TABLE IF EXISTS route_m1;

CREATE TABLE route_m1 AS
SELECT
  ST_LineFromEncodedPolyline(
    'ppjfF{zwtZeCYMGAOn@iLwS}BiMsAoAMB]p@uLFqBh@sJR_DTuDf@gJv@yMb@wH`@oIl@wJf@sJ|@cLnAqPvAaWd@yHVoDT}E^}GPqDZwFt@eMp@sNLwBJmBDUN}CHeBBg@RqDl@{KTiDz@uNJaC`@iGJgAd@aGVqD`@uFx@{MVaEh@yJ~@aPR{CXwEl@uKlAgTfAaRZaFf@mJB{CCsAYmCc@qBa@sAOe@w@iBmDqH_C}EgGmMyAuCeAoB]o@YGCCgByBe@B}CYqBMcAC_BEcECc@?MQsGN{BDmNDqVIeYOoIEgCDyCJeCTwARQBuAN{Bd@}D`Ac@H}Ab@eMxCmFhAeEv@uB^wAPoHz@uAJmBLmEVqCJuEJmNTaJIiCI}DSwFe@aEc@mDg@}E}@eCk@iCm@}@Sk@SQGyLqDeF{A_Bg@mGmBeIaCQJgDk@mBYgAIu@EcBCwBIeAI]Me@E}@Me@G@MHsA`@iFrA{Q?Wh@_Gx@oLf@_HZcEF}Ad@aEjAaF~DiQ`BmHl@iCv@oD~EyTlAqFxCcM~@mE~AeH`AcEnBcIbAcElAoFpByIx@yDz@gE~CoMb@iB_@UiCyC_@c@z@sAP]h@sB`AkE'
  )::geometry(LineString, 4326) AS geom;

