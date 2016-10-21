#define FILTERSCRIPT

#include <a_samp>
#include <sscanf2>
#include <colandreas>
#include <3DTryg>

new files[][]={"Maps/BC.foliage", "Maps/FC.foliage", "Maps/LS.foliage", "Maps/LV.foliage", "Maps/SF.foliage", "Maps/RC.foliage", "Maps/TR.foliage", "Maps/other.foliage"};

new buffer[1024];

public OnFilterScriptInit()
{
	CA_Init();
	new time = GetTickCount();
	print("Starting.");
	new 
		File:f_in,
		File:f_out,
		line,
		type[12],
		model,
		Float:x,
		Float:y,
		Float:z,
		Float:rx,
		Float:ry,
		Float:rz,
		Float:streamdistance
	;
	for(new i; i < sizeof(files); ++i)
	{
		if(!fexist(files[i]))
			continue;
		f_out = fopen(files[i], io_write);
		f_in = fopen(files[i]);
		line = -1;
		while(fread(f_in, buffer))
		{
			++line;
			if(sscanf(buffer, "s[12]fff", type, x, y, streamdistance))
			{
				printf("Failed to load object on file %s line %d", files[i], line);
				continue;
			}
			// Get rx and ry
			GetGroundRotation(x, y, 2.0, rx, ry);
			// Get z
			CA_FindZ_For2DCoord(x, y, z);
			// Get model
			model = _getModel(type);
			format(buffer, sizeof(buffer), "CreateDynamicObject(%d, %f, %f, %f, %f, %f, %f, .streamdistance = %f);\r\n", model, x, y, z, rx, ry, rz, streamdistance);
			fwrite(f_out, buffer);
		}
		fclose(f_out);
		fclose(f_in);
	}
	printf("Done, with %d ms", GetTickCount() - time);
}

new
obj_arr_water[] = {1242, 1242},
obj_arr_roads[] = {18862, 647, 692, 759, 760, 762, 800, 801, 802, 803, 804, 805, 806, 807, 808, 809, 810, 811, 812, 813, 814, 815, 816, 818, 819, 820, 821, 822, 823, 824, 825, 826, 827},
obj_arr_darkforest[] = {647, 692, 759, 760, 762, 800, 801, 802, 803, 804, 805, 806, 807, 808, 809, 810, 811, 812, 813, 814, 815, 816, 818, 819, 820, 821, 822, 823, 824, 825, 826, 827},
obj_arr_lightforest[] = {654, 655, 656, 657, 658, 659, 660, 661},
obj_arr_desert[] = {647, 692, 759, 760, 762, 800, 801, 802, 803, 804, 805, 806, 807, 808, 809, 810, 811, 812, 813, 814, 815, 816, 818, 819, 820, 821, 822, 823, 824, 825, 826, 827},
obj_arr_grassplanes[] = {647, 692, 759, 760, 762, 800, 801, 802, 803, 804, 805, 806, 807, 808, 809, 810, 811, 812, 813, 814, 815, 816, 818, 819, 820, 821, 822, 823, 824, 825, 826, 827};

new global_model;
_getModel(type[12])
{
	static function[17];
	format(function, sizeof(function), "type_%s", type);
	CallLocalFunction(function, "");
	return global_model;
}
#define T:%0() forward type_%0(); public type_%0() {global_model = obj_arr_%0[random(sizeof(obj_arr_%0))];}

T:water()
T:roads()
T:darkforest()
T:lightforest()
T:desert()
T:grassplanes()