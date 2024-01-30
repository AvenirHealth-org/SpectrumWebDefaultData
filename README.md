# SpectrumWebDefaultData

SourceData is the source files, usually in CSV or XLSX format, that are supplied to us from internal and external sources.
JSONData is the processed, formatted data that is used by our web servers, in JSON format.
Scripts is the code that does the processing into JSON.

The scripts are run from __main__ as a module, this is important to do otherwise some references may break. (os.cwd() in particular)