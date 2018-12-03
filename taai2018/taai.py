
from fun import core
import time
from selenium.common.exceptions import StaleElementReferenceException, WebDriverException

import pdfkit
# needs system wide installation of:
# brew install Caskroom/cask/wkhtmltopdf


driver = core.firefox(dr='/GitHub/taaipdf/driver/geckodriver', fi='/GitHub/taaipdf/pdfs')


def pdfc(d):
    d.get('http://taai2018.asia.edu.tw/papers/?fbclid=IwAR2eNq-4CWfXD4Q_rF-SuSoXKNbeciCDFq3ZQNOFaS4NTkjYs'
          'BFxIAu5Z48#!/toc/0')

    j = 0
    while j < 1000:
        try:
            # pdf = d.find_elements_by_class_name('pull-right ng-binding')
            pdf = d.execute_script("return document.getElementsByClassName('pull-right ng-binding')")
            option = d.execute_script("return document.getElementsByClassName('pull-right ng-binding').length")

            print('Number of pdfs:', option)
            if int(option) == 90:
                break
            else:
                j += 1
                continue
        except (StaleElementReferenceException, WebDriverException):
            time.sleep(0.1)
            j += 1
            continue

    # download webpage as pdf
    try:
        pdfkit.from_url('http://taai2018.asia.edu.tw/papers/?fbclid=IwAR2eNq-4CWfXD4Q_rF-SuSoXKNbeciCDFq3ZQNOFaS4NTkjYs'
                        'BFxIAu5Z48#!/toc/0', '/Users/ch.ke/GitHub/taaipdf/pdfs/content.pdf')
    except:
        print('# Some errors found, rmb to check content.pdf!')
        pass

    # download each file
    page = []
    nopdf = []
    for i in range(0, len(pdf)):
        j = 0
        while j < 1000:
            try:
                pgn = d.execute_script("return document.getElementsByClassName('pull-right ng-binding')[" +
                                       str(i) + "].textContent")
                pdf[i].click()
                e = 0
                while True:
                    try:
                        parent = d.window_handles[0]
                        popup = d.window_handles[1]
                        break
                    except IndexError:
                        time.sleep(0.1)
                        e += 1
                        if e < 50:
                            continue
                        else:
                            print('PDF not found after', str(e * 0.1), 'secs')
                            popup = 'no'
                            nopdf.append(popup)
                            break
                if popup == 'no':
                    break
                if parent != popup:
                    d.switch_to_window(popup)
                    url = 'about:blank'
                    while url == 'about:blank':
                        url = driver.current_url
                        time.sleep(0.1)
                    doc_id = url.split("/")[-2]
                    print(doc_id)
                    durl = "https://drive.google.com/uc?id={0}&export=download".format(doc_id)
                    print(durl)
                    print(pgn)
                    page.append(pgn)
                    print('clicking:', i)
                    # last pdf has direct link
                    if int(i) == 89:
                        core.dlreq(url, str('375(' + pgn + ')'))
                    else:
                        core.dlreq(durl, pgn)
                    d.close()
                d.switch_to.window(parent)
                break
            except (StaleElementReferenceException, WebDriverException):
                time.sleep(0.1)
                j += 1
                continue

    print('Number of articles with pdf files:', str(len(pdf) - len(nopdf)))
    return page


# for program timing
start_time = time.time()

pdf = pdfc(driver)

# print time crawler took
print("Crawler ran for: {0} seconds ({1} mins)".format(str(round(time.time() - start_time, 2)),
                                                       str(round((time.time() - start_time)/60))))
