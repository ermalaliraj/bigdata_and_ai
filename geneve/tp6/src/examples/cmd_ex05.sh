python2.7 apply_composition.py -i ../examples/data/in/data_to_comp.txt -m dilation --lambda 2 -a ../examples/data/out/ex01.pkl -o ../examples/data/out/ --output_format dm
python2.7 apply_composition.py -i ../examples/data/in/data_to_comp.txt -m mult -a ../examples/data/out/ex01.pkl -o ../examples/data/out/ --output_format dm
python2.7 apply_composition.py -i ../examples/data/in/data_to_comp.txt --load_model ../examples/data/out/model01.pkl -a ../examples/data/out/ex01.pkl -o ../examples/data/out/ --output_format dm
python2.7 apply_composition.py -i ../examples/data/in/data_to_comp2.txt --load_model ../examples/data/out/model01.pkl -a ../examples/data/out/ex01.pkl,../examples/data/out/PER_SS.ex05.pkl -o ../examples/data/out/ --output_format dm
