#          import pytest
#          
#          def soma(a,b):
#              return a+b
#          
#          def dividir(a,b):
#              if b == 0:
#                  raise ZeroDivisionError("pode não")
#              return a/b
#          
#          @pytest.fixture
#          def usuario():
#              return "joão"
#          
#          @pytest.mark.parametrize(
#                  "a,b,result",
#                  [
#                      (1, 5, 6),
#                      (5, 3, 8),
#                      (6, 8, 14)
#                  ]
#          )
#          def test_soma(a,b,result):
#              assert soma(a, b) == result
#          
#          def test_nome(usuario):
#              assert usuario == "joão"
#          
#          def test_dividir_zero():
#              with pytest.raises(ZeroDivisionError, match="pode não"):
#                  dividir(10,0)