# Detect the julianDay from image filename
def date_of_modis(filename):
    julianDay = filename[-37:-30]
    [theyear, therealmonth, therealday] = rejulia(int(julianDay[0:4]), int(julianDay[4:]))
    return theyear, therealmonth, therealday

# Change julian day to normal day (year month day)
def rejulia(theyear, theday):
    leapyear = theyear % 4
    if leapyear > 0:
        leap = 0
    else:
        if theyear % 100 == 0 and theyear % 400 != 0:
            leap = 0
        else:
            leap = 1

    if leap == 0:
        if theday <= 31:
            therealmonth = 1
            therealday = theday

        if theday >= 32 and theday <= 59:
            therealmonth = 2
            therealday = theday - 31

        if theday >= 60 and theday <= 90:
            therealmonth = 3
            therealday = theday - 59

        if theday >= 91 and theday <= 120:
            therealmonth = 4
            therealday = theday - 90

        if theday >= 121 and theday <= 151:
            therealmonth = 5
            therealday = theday - 120

        if theday >= 152 and theday <= 181:
            therealmonth = 6
            therealday = theday - 151

        if theday >= 182 and theday <= 212:
            therealmonth = 7
            therealday = theday - 181

        if theday >= 213 and theday <= 243:
            therealmonth = 8
            therealday = theday - 212

        if theday >= 244 and theday <= 273:
            therealmonth = 9
            therealday = theday - 243

        if theday >= 274 and theday <= 304:
            therealmonth = 10
            therealday = theday - 274

        if theday >= 305 and theday <= 334:
            therealmonth = 11
            therealday = theday - 305

        if theday >= 335 and theday <= 365:
            therealmonth = 12
            therealday = theday - 334

    if leap == 1:
        if theday <= 31:
            therealmonth = 1
            therealday = theday

        if theday >= 32 and theday <= 60:
            therealmonth = 2
            therealday = theday - 31

        if theday >= 61 and theday <= 91:
            therealmonth = 3
            therealday = theday - 60

        if theday >= 92 and theday <= 121:
            therealmonth = 4
            therealday = theday - 91

        if theday >= 122 and theday <= 152:
            therealmonth = 5
            therealday = theday - 121

        if theday >= 153 and theday <= 182:
            therealmonth = 6
            therealday = theday - 152

        if theday >= 183 and theday <= 213:
            therealmonth = 7
            therealday = theday - 182

        if theday >= 214 and theday <= 244:
            therealmonth = 8
            therealday = theday - 213

        if theday >= 245 and theday <= 274:
            therealmonth = 9
            therealday = theday - 244

        if theday >= 275 and theday <= 305:
            therealmonth = 10
            therealday = theday - 275

        if theday >= 306 and theday <= 335:
            therealmonth = 11
            therealday = theday - 306

        if theday >= 336 and theday <= 366:
            therealmonth = 12
            therealday = theday - 335

    return theyear, therealmonth, therealday

    # filename = '/mnt/hgfs/Data/qhl/MCD15A3.005/MCD15A3A2002185/MCD15A3A2002059_Fpar_1km_MOD_Grid_MOD15A2.tif'
    # julianDay = filename[-37:-30]
    # print julianDay
    # print int(julianDay[0:4])
    # print int(julianDay[4:])
    # print rejulia(int(julianDay[0:4]), int(julianDay[4:]))
