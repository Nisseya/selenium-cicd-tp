## Première partie (copié-collé de code)

Cela fonctionne, j'ai du modifier pytest car au début les erreurs étaient des os error:

ERROR tests\test_selenium.py::TestCalculator::test_page_loads - OSError: [WinError 193] %1 is not a valid Win32 application
ERROR tests\test_selenium.py::TestCalculator::test_addition - OSError: [WinError 193] %1 is not a valid Win32 application
ERROR tests\test_selenium.py::TestCalculator::test_division_by_zero - OSError: [WinError 193] %1 is not a valid Win32 application
ERROR tests\test_selenium.py::TestCalculator::test_all_operations - OSError: [WinError 193] %1 is not a valid Win32 application


Cela vient de Chromedriver().install() qui renvoie un chemin de fichier qui ne finit pas par chrome.exe donc impossible de démarrer.

On modifie donc le code:
```python 
   
    path = ChromeDriverManager().install()
    if sys.platform.startswith("win") and not path.endswith("chromedriver.exe"):
        path = os.path.join(os.path.dirname(path), "chromedriver.exe")

    service = Service(path)

```


Et on règle l'erreur de drivers et d'autorisations navigateur, en démarrant un serveur local.

```bash

cd src
python -m http.server 8000

```


## Ecriture nouveaux tests 

#### Flottants:
- On écrit des tests pour les 4 différentes opérations
- Aucun ne fonctionne

On modifie le HTML pour que les input type passent de number à text (dans le js c'est parsé pour etre converti en float dans tous les cas).
Ce qui est marrant car selon la doc, type number accepte le point en tant que délimiteur de float, donc je ne sais pas trop pourquoi.
En tout cas les tests sont passés c'est ce qui compte.

Maintenant les cas fonctionnent:

```bash
tests/test_selenium.py::TestCalculator::test_page_loads
DevTools listening on ws://127.0.0.1:55146/devtools/browser/f2ba16d6-117c-4d84-b63d-8443ee06e356
PASSED                                                                                                                                     [ 11%]
tests/test_selenium.py::TestCalculator::test_addition PASSED                                                                                                                                       [ 22%]
tests/test_selenium.py::TestCalculator::test_division_by_zero PASSED                                                                                                                               [ 33%]
tests/test_selenium.py::TestCalculator::test_all_operations WARNING: All log messages before absl::InitializeLog() is called are written to STDERR
I0000 00:00:1751363609.989130   27632 voice_transcription.cc:58] Registering VoiceTranscriptionCapability
PASSED                                                                                                                                 [ 44%]
tests/test_selenium.py::TestCalculator::test_page_load_time PASSED                                                                                                                                 [ 55%]
tests/test_selenium.py::TestCalculator::test_division_by_float PASSED                                                                                                                              [ 66%]
tests/test_selenium.py::TestCalculator::test_multiplication_by_float PASSED                                                                                                                        [ 77%]
tests/test_selenium.py::TestCalculator::test_sum_by_float PASSED                                                                                                                                   [ 88%]
tests/test_selenium.py::TestCalculator::test_sub_by_float PASSED             
```

et le code des tests (on aurait peut etre tout pu mettre dans le meme test mais oklm)

```python
def test_division_by_float(self, driver):
    """Test 6: Tester la division avec float"""
    driver.get(BASE_URL)
    driver.find_element(By.ID, "num1").clear()
    driver.find_element(By.ID, "num1").send_keys("1.5")
    driver.find_element(By.ID, "num2").clear()
    driver.find_element(By.ID, "num2").send_keys("0.3")
    select = Select(driver.find_element(By.ID, "operation"))
    select.select_by_value("divide")
    driver.find_element(By.ID, "calculate").click()
    result = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.ID, "result"))
    )
    assert "Résultat: 5" in result.text

def test_multiplication_by_float(self, driver):
    """Test 7: Tester la multiplication float"""
    driver.get(BASE_URL)
    driver.find_element(By.ID, "num1").clear()
    driver.find_element(By.ID, "num1").send_keys("1.5")
    driver.find_element(By.ID, "num2").clear()
    driver.find_element(By.ID, "num2").send_keys("2")
    select = Select(driver.find_element(By.ID, "operation"))
    select.select_by_value("multiply")
    driver.find_element(By.ID, "calculate").click()
    result = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.ID, "result"))
    )
    assert "Résultat: 3" in result.text

def test_sum_by_float(self, driver):
    """Test 8: Tester l'addition float"""
    driver.get(BASE_URL)
    driver.find_element(By.ID, "num1").clear()
    driver.find_element(By.ID, "num1").send_keys("1.5")
    driver.find_element(By.ID, "num2").clear()
    driver.find_element(By.ID, "num2").send_keys("0.3")
    select = Select(driver.find_element(By.ID, "operation"))
    select.select_by_value("add")
    driver.find_element(By.ID, "calculate").click()
    result = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.ID, "result"))
    )
    assert "Résultat: 1.8" in result.text

def test_sub_by_float(self, driver):
    """Test 9: Tester la soustraction float"""
    driver.get(BASE_URL)
    driver.find_element(By.ID, "num1").clear()
    driver.find_element(By.ID, "num1").send_keys("1.5")
    driver.find_element(By.ID, "num2").clear()
    driver.find_element(By.ID, "num2").send_keys("0.3")
    select = Select(driver.find_element(By.ID, "operation"))
    select.select_by_value("subtract")  # ← Fix here
    driver.find_element(By.ID, "calculate").click()
    result = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.ID, "result"))
    )
    assert "Résultat: 1.2" in result.text

```


#### Tests nombres négatifs

Les nombres négatifs fonctionnent très bien directement, avec le changement number->text fait précédemment.

**Code des tests**

```python
def test_division_with_negative(self, driver):
    """Test 10: Division avec un nombre négatif"""
    driver.get(BASE_URL)
    driver.find_element(By.ID, "num1").clear()
    driver.find_element(By.ID, "num1").send_keys("-6")
    driver.find_element(By.ID, "num2").clear()
    driver.find_element(By.ID, "num2").send_keys("2")
    select = Select(driver.find_element(By.ID, "operation"))
    select.select_by_value("divide")
    driver.find_element(By.ID, "calculate").click()
    result = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.ID, "result"))
    )
    assert "Résultat: -3" in result.text


def test_multiplication_with_negative(self, driver):
    """Test 11: Multiplication avec un nombre négatif"""
    driver.get(BASE_URL)
    driver.find_element(By.ID, "num1").clear()
    driver.find_element(By.ID, "num1").send_keys("-3")
    driver.find_element(By.ID, "num2").clear()
    driver.find_element(By.ID, "num2").send_keys("2")
    select = Select(driver.find_element(By.ID, "operation"))
    select.select_by_value("multiply")
    driver.find_element(By.ID, "calculate").click()
    result = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.ID, "result"))
    )
    assert "Résultat: -6" in result.text


def test_sum_with_negative(self, driver):
    """Test 12: Addition avec un nombre négatif"""
    driver.get(BASE_URL)
    driver.find_element(By.ID, "num1").clear()
    driver.find_element(By.ID, "num1").send_keys("-1.5")
    driver.find_element(By.ID, "num2").clear()
    driver.find_element(By.ID, "num2").send_keys("0.3")
    select = Select(driver.find_element(By.ID, "operation"))
    select.select_by_value("add")
    driver.find_element(By.ID, "calculate").click()
    result = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.ID, "result"))
    )
    assert "Résultat: -1.2" in result.text


def test_sub_with_negative(self, driver):
    """Test 13: Soustraction avec un nombre négatif"""
    driver.get(BASE_URL)
    driver.find_element(By.ID, "num1").clear()
    driver.find_element(By.ID, "num1").send_keys("-1.5")
    driver.find_element(By.ID, "num2").clear()
    driver.find_element(By.ID, "num2").send_keys("0.5")
    select = Select(driver.find_element(By.ID, "operation"))
    select.select_by_value("subtract")
    driver.find_element(By.ID, "calculate").click()
    result = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.ID, "result"))
    )
    assert "Résultat: -2" in result.text

```

Résultat

```bash

tests/test_selenium.py::TestCalculator::test_addition PASSED                                                                                                                                       [ 15%]
tests/test_selenium.py::TestCalculator::test_division_by_zero PASSED                                                                                                                               [ 23%]
tests/test_selenium.py::TestCalculator::test_all_operations WARNING: All log messages before absl::InitializeLog() is called are written to STDERR
I0000 00:00:1751364302.281595   17220 voice_transcription.cc:58] Registering VoiceTranscriptionCapability
PASSED                                                                                                                                 [ 30%]
tests/test_selenium.py::TestCalculator::test_page_load_time PASSED                                                                                                                                 [ 38%]
tests/test_selenium.py::TestCalculator::test_division_by_float PASSED                                                                                                                              [ 46%]
tests/test_selenium.py::TestCalculator::test_multiplication_by_float PASSED                                                                                                                        [ 53%]
tests/test_selenium.py::TestCalculator::test_sum_by_float PASSED                                                                                                                                   [ 61%]
tests/test_selenium.py::TestCalculator::test_sub_by_float PASSED                                                                                                                                   [ 69%]
tests/test_selenium.py::TestCalculator::test_division_with_negative PASSED                                                                                                                         [ 76%]
tests/test_selenium.py::TestCalculator::test_multiplication_with_negative PASSED                                                                                                                   [ 84%]
tests/test_selenium.py::TestCalculator::test_sum_with_negative PASSED                                                                                                                              [ 92%]
tests/test_selenium.py::TestCalculator::test_sub_with_negative PASSED                                                                                                                              [100%]

```


## Refactorisation du code

On améliore le calculator_page.py, pour remplir directement le form en une seule fonction.
Cela permet de faire des tests en 3 lignes.

Voici le fill form:

```python
def fill_form(self, num1, num2, operation):
    self.clear_fields()
    self.driver.find_element(By.ID, "num1").send_keys(str(num1))
    self.driver.find_element(By.ID, "num2").send_keys(str(num2))
    select = Select(self.driver.find_element(By.ID, "operation"))
    select.select_by_value(operation)
    self.driver.find_element(By.ID, "calculate").click()
```

cette fonction la va etre la base de la plupart des tests:

Voici un extrait de tests refactorisés:

```python

    # Floats
    def test_division_by_float(self, page):
        page.fill_form(1.5, 0.3, "divide")
        assert "Résultat: 5" in page.get_result()

    def test_multiplication_by_float(self, page):
        page.fill_form(1.5, 2, "multiply")
        assert "Résultat: 3" in page.get_result()

    def test_sum_by_float(self, page):
        page.fill_form(1.5, 0.3, "add")
        assert "Résultat: 1.8" in page.get_result()

    def test_sub_by_float(self, page):
        page.fill_form(1.5, 0.3, "subtract")
        assert "Résultat: 1.2" in page.get_result()

```

Les tests pasent tous avec la refactorisation, on est bons.

## Workflow 