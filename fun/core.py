import pathlib
from selenium import webdriver
from os.path import expanduser as ep
import requests


def dlreq(url, name):
    response = requests.get(url)
    pdf = response.content
    cname = '/Users/ch.ke/GitHub/taaipdf/pdfs/' + name + '.pdf'
    with open(cname, 'wb') as f:
        f.write(pdf)


def firefox(dr, fi):
    firefox_driver = ep('~') + dr

    # create data download folder
    pathlib.Path(ep('~') + fi).mkdir(parents=True, exist_ok=True)

    profile = webdriver.FirefoxProfile()
    profile.set_preference("browser.privatebrowsing.autostart", True)
    profile.set_preference("browser.download.folderList", 2)
    profile.set_preference("browser.download.manager.showWhenStarting", False)
    # download location
    profile.set_preference("browser.download.useDownloadDir", True)
    profile.set_preference("browser.download.dir", ep('~') + fi)
    ftypes = ("application/download,application/x-7z-compressed,text/html,text/plain,application/pdf,image/bmp,"
              "application/x-bzip,application/x-csh,text/x-c,text/css,text/csv,image/gif,video/h261,"
              "image/x-icon,text/x-java-source,java,application/javascript,application/json,"
              "image/jpeg,image/pjpeg,application/x-latex,application/vnd.ms-excel,"
              "application/vnd.ms-excel.addin.macroenabled.12,application/vnd.ms-excel.sheet.binary.macroenabled.12,"
              "application/vnd.ms-excel.template.macroenabled.12,application/vnd.ms-excel.sheet.macroenabled.12,"
              "application/vnd.openxmlformats-officedocument.presentationml.presentation,"
              "application/vnd.openxmlformats-officedocument.presentationml.slide,"
              "application/vnd.openxmlformats-officedocument.presentationml.slideshow,"
              "application/vnd.openxmlformats-officedocument.presentationml.template,"
              "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet,"
              "application/vnd.openxmlformats-officedocument.spreadsheetml.template,"
              "application/vnd.openxmlformats-officedocument.wordprocessingml.document,"
              "application/vnd.openxmlformats-officedocument.wordprocessingml.template,"
              "application/vnd.ms-powerpoint,application/vnd.ms-powerpoint.addin.macroenabled.12,"
              "application/vnd.ms-powerpoint.slide.macroenabled.12,"
              "application/vnd.ms-powerpoint.presentation.macroenabled.12,"
              "application/vnd.ms-powerpoint.slideshow.macroenabled.12,"
              "application/vnd.ms-powerpoint.template.macroenabled.12,"
              "application/msword,application/vnd.ms-word.document.macroenabled.12,"
              "application/vnd.ms-word.template.macroenabled.12,application/x-mswrite,application/vnd.ms-xpsdocument,"
              "video/mj2,audio/mpeg,video/mpeg,application/mp21,audio/mp4,video/mp4,application/mp4,"
              "audio/ogg,video/ogg,application/vnd.oasis.opendocument.image,"
              "application/vnd.oasis.opendocument.presentation,application/vnd.oasis.opendocument.spreadsheet,"
              "application/vnd.oasis.opendocument.text,image/png,image/x-citrix-png,image/x-png,video/quicktime,"
              "text/richtext,image/svg+xml,image/x-rgb,application/zip,application/octet-stream")
    profile.set_preference("browser.helperApps.neverAsk.saveToDisk", ftypes)
    profile.set_preference("pdfjs.disabled", "true")
    profile.update_preferences()
    driver = webdriver.Firefox(executable_path=firefox_driver, firefox_profile=profile)
    # driver.set_window_size(1390, 850)
    driver.maximize_window()

    return driver
