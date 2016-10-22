#define FILTERSCRIPT

#include <a_samp>
#include <sscanf2>
#include <colandreas>
#include <3DTryg>
#include <modelsizes>

new files[][]={"Maps/BC.foliage", "Maps/FC.foliage", "Maps/LS.foliage", "Maps/LV.foliage", "Maps/SF.foliage", "Maps/RC.foliage", "Maps/TR.foliage", "Maps/other.foliage"};
new filesout[][]={"Maps/BC.map", "Maps/FC.map", "Maps/LS.map", "Maps/LV.map", "Maps/SF.map", "Maps/RC.map", "Maps/TR.map", "Maps/other.map"};

new buffer[1024];
forward Float:_getStreamDistance(model);
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
		f_out = fopen(filesout[i], io_write);
		f_in = fopen(files[i]);
		line = -1;
		while(fread(f_in, buffer))
		{
			++line;
			if(sscanf(buffer, "s[12]ff", type, x, y))
			{
				printf("Failed to load object on file %s line %d", files[i], line);
				continue;
			}
			if(IsPointInWater(x, y))
			{
				printf("[Warning]Water point x = %f y = %f", x, y);
				continue;
			}
			// Get model
			model = _getModel(type);
			// Get z
			CA_FindZ_For2DCoord(x, y, z);
			if(!IsPointInUnderground(x, y, z))
			{
				printf("[Warning]Not ground point x = %f y = %f", x, y);
				continue;
			}
			// Get rx and ry
			if(IsTree(model))
			{
				rx = ry = 0.0;
				z -= 0.5;
			}
			else
				GetGroundRotation(x, y, 2.0, rx, ry);

			streamdistance = _getStreamDistance(model);
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
obj_arr_roads[] = {
	18862, 744, 745, 746, 747, 748, 749, 450, 816, 828, 905, 701, 702, 811, 815, 818, 864, 863, 865, 866, 875, 876, 760
},
obj_arr_darkforest[] = {
664,670,685,686,687,693,696,697,704,719,720,721,723,725,881, // trees
654, 655, 656, 689, 664, 696, 694, 695, 697, 693, 698, 690, 671, 658, 664, 789, 790, 791, 18272, 18273, 18270, 18268, 18271, 18269, 698, 715, 705, 722, 723, 724, 725, 721, 720, 719
},
obj_arr_lightforest[] = {
615,617,654,655,656,657,658,726,727,729,730,731,732,733,734,735,763,764,765,766,770,771,779, // trees
615, 616, 617, 618, 654, 655, 656, 657, 658, 659, 660, 661, 671, 672, 673, 676, 691, 16060, 16061, 775, 776, 777, 892, 703, 713, 705, 709, 706, 707, 708

},
obj_arr_desert[] = {
674,676,680,681,773,651, // trees
734, 735, 764, 692, 650, 653, 855, 815, 760, 759, 857, 871, 827, 864, 865, 866
},
obj_arr_grassplanes[] = {
	669,671,672,691,703,705,706,707,708,767,768,769,772,774,775,776,777,778,780,781,782, // trees
	8403, 728, 762, 801, 804, 812, 822, 821, 823, 825, 873, 872, 859, 871, 862, 677, 682, 701, 856, 826, 806, 789, 715 // objetos diversos
};
IsTree(model)
{
	switch(model)
	{
		case 615,617,651,654,655,656,657,658,664,669,670,671,672,674,676,680,681,685,686,687,691,693,696,697,703,704,705,706,707,708,719,720,721,723,725,726,727,729,730,731,732,733,734,735,763,764,765,766,767,768,769,770,771,772,773,774,775,776,777,778,779,780,781,782,881:
		{
			return true;
		}
	}
	return false;
}
Float:_getStreamDistance(model)
{
	new Float:dist;
	static const Float:arr[4][2] = {
		{0.0, 40.0},
		{5.0, 50.0},
		{20.0, 100.0},
		{50.0, 150.0}
	};
	for(new iter; iter < sizeof(arr); iter++){
		if(GetColSphereRadius(model) > arr[iter][0])
		{
			dist = arr[iter][1];
		}
	}
	return dist;
}

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