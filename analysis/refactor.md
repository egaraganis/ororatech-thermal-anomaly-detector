# Refactoring Thermal Anomaly Detection

```python
class NetCDFSatelliteOverpassData() {
    observationNetCDFData
    geolocationDataCDFData

    validateOverpassData(observationDataFile, geolocationDataFile)
    getObservationNetCDFData()
    getGeolocationNetCDFData()
}

class ThermalAnomalyDetector() {
    NetCDFSatelliteOverpassData satelliteOverpassData

    filterHotpixelCandidatesBasedOnTheshold(thresholdSupplier)
    clusterHotpixelCandidatesBasedOnGeospatialCoords(hotpixelCandidates)
    detectThermalAnomaliesAndReturnGeoJSONResponse()
    ...
}
```

Hm...Not sure the implementation will favor from OOP paradigm. While encapsulation might be of use, there are a lot of phases that I don't feel that they can be abstracted right away. For example both clustering, convex and concave creation can either happen on both geospatial coords or pixel/scan dimensions. Most propably a FP-style with some  declarative testing would make more sense at this stage of the implementation.
