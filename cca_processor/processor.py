import zipfile
import csv
from cStringIO import StringIO


def documents(name, archive):
    """Compiles the list of content to be indexed"""
    data = {}
    try:
        data = mess_with_zipfile(archive)
        if 'results' in data:
            return process_data(data['results'])
    except IOError:
        data['error'] = 'Could not read %s' % archive
    except zipfile.BadZipfile:
        data['error'] = 'File %s is not a zip archive ' % archive
    except zipfile.LargeZipFile:
        data['error'] = 'File %s is too big ' % archive
    except IndexError:
        data['error'] = "Apparently there's no CSV file in the archive"
    except KeyError:
        data['error'] = 'A key error happened'
    except Exception as e:
        data['error'] = 'Another exception %s ' % e
    return data


def process_data(data):
    """Massage the data, add/remove/modify fields"""
    for ndx, value in enumerate(data):
        value['_id'] = "%s-%s" % (value['CFPB Filename'], value['ID'])
        value['Agreement Description'] = value['Agreement Description'].decode('ISO-8859-1')
        value['Issuer Name'] = value['Issuer Name'].decode('ISO-8859-1')
        if value['Effective Date'] == '1900-01-00':
            value['Effective Date'] = '1900-01-01'
        # remove fields we're not interested in
        data[ndx] = value
    return data


def mess_with_zipfile(archive):
    """Read data from csv file inside a zip archive"""
    with zipfile.ZipFile(archive, 'r') as zf:
        #FIXME: right now will only process the first CSV file it finds
        csvfile = [path for path in zf.namelist() if path.endswith('.csv')][0]
        csvreader = csv.DictReader(StringIO(zf.read(csvfile)))
        data = []
        for row in csvreader:
            data.append(row)
        return {'results': data}
