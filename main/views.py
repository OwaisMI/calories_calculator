from typing import Final
from django.shortcuts import render, redirect
from .models import *
from .forms import *
from django.db.models import *
# Create your views here.

def home(request):
    #When the user clicks on the website, the homepage shows up
    if request.method == 'GET':
        form=CalorieCal(initial={'HeightChoice': 'CM'})
        return render(request, 'main/home.html',{'form':form})

    #If the user fills and submits the form
    if request.method == 'POST':
        form=CalorieCal(request.POST)
        #Taking Inputs from user in Post method
        if form.is_valid():
            Age=form.cleaned_data['Age']
            Weight=float(form.cleaned_data['Weight'])
            Height=form.cleaned_data['Height']
            Height_feet=form.cleaned_data['Height_1st']
            Height_inches=form.cleaned_data['Height_2nd']
            Gender=form.cleaned_data['Gender']
            Activity=form.cleaned_data['Activity']
            
            if Height_feet is not None:
                Height_feet = float(Height_feet)
            if Height_inches is not None:
                Height_inches = float(Height_inches)

            #Choices for weight and height
            WeightChoice=form.cleaned_data['WeightChoice']
            
            HeightChoice=form.cleaned_data['HeightChoice']
            
            if(HeightChoice == 'Feet' and Gender == 'Male' and WeightChoice == 'LB'):
                Height_feet = (Height_feet*12)
                Height_metric= Height_feet+Height_inches

                BMR = (Weight*4.536) + (Height_metric*14.88) - (Age*5) + (5)

            if(HeightChoice == 'Feet' and Gender == 'Male' and WeightChoice == 'KG'):
                Height_feet = (Height_feet*12)
                Height_metric= Height_feet+Height_inches

                BMR = (Weight*10) + (Height_metric*14.88) - (Age*5) + (5)

            elif(HeightChoice == 'Feet' and Gender == 'Female' and WeightChoice == 'LB'):
                Height_feet = (Height_feet*12)
                Height_metric= Height_feet+Height_inches
                BMR = round((Weight*4.536) + (Height_metric*15.88) - (Age*5) - (161))

            elif(HeightChoice == 'Feet' and Gender == 'Female' and WeightChoice == 'KG'):
                Height_feet = (Height_feet*12)
                Height_metric= Height_feet+Height_inches
                BMR = round((Weight*10) + (Height_metric*15.88) - (Age*5) - (161))

            # Calculation According to gender
            elif (HeightChoice == 'CM' and Gender == 'Male' and WeightChoice == 'KG'):
                BMR =round((Weight*10) + (Height*6.25) - (Age*5) + (5))
            elif (HeightChoice == 'CM' and Gender == 'Female' and WeightChoice == 'KG'):
                BMR =round((Weight*10 )+ (Height*6.25) - (Age*5) - (161))

            elif (HeightChoice == 'CM' and Gender == 'Male' and WeightChoice == 'LB'):
                BMR =round((Weight*4.536) + (Height*6.25) - (Age*5) + (5))
            elif (HeightChoice == 'CM' and Gender == 'Female' and WeightChoice == 'LB'):
                BMR =round((Weight*4.536)+ (Height*6.25) - (Age*5) - (161))

            #Calculation According to Activity Level

            if (Activity == '1'):
                Calories=(BMR*1.3)
            elif (Activity == '2'):
                Calories=(BMR*1.5)
            elif (Activity == '3'):
                Calories=(BMR*1.7)

            #Drop down for checking if its for Loosing weight or gaining muscle
            TypeOfCal=form.cleaned_data['CalType']
            
            #Cutting Calories
            if (TypeOfCal == 'Losing Weight'):
                Calorie=round(Calories-250)
            elif (TypeOfCal == 'Gaining Muscle'):
                #Surplus Calories
                Calorie=round(Calories+250)

            if(WeightChoice == 'KG'):
                #Macros For Metric
                Proteins=round(Weight*2.2,2)
                Fats=round(Proteins*0.4,2)

                CalFromProteins=Proteins*4
                CalFromFats=Fats*9

                CalFromCarbs=Calories-CalFromFats-CalFromProteins
                Carbs=round(CalFromCarbs/4,2)

            elif(WeightChoice == 'LB'):
                Proteins=round(Weight)
                Fats=round(Proteins*0.4,2)

                CalFromProteins=Proteins*4
                CalFromFats=Fats*9

                CalFromCarbs=Calories-CalFromFats-CalFromProteins

                Carbs=round(CalFromCarbs/4,2)
   
    context = {'form':form, 'Calorie':Calorie, 'Proteins': Proteins,'Carbs': Carbs, 'Fats': Fats}
    return render(request, 'main/home.html',context)

def DietPlan(request):
    Calories=int(request.POST.get('Calories', 0)) #Just changed to integer from float
    Proteins=float(request.POST.get('Proteins',0))
    Carbs=float(request.POST.get('Carbs',0))
    Fats=float(request.POST.get('Fats',0))
    
    breakfast_cal,breakfast_protein,breakfast_carbs,\
        breakfast_fats=percentage(20,calories=Calories,protein=Proteins,\
        carbs=Carbs,fats=Fats)
    # print("This is breakfastcal at line 119", breakfast_cal) CORRECT

    lunch_cal,lunch_protein,lunch_carbs,\
        lunch_fats=percentage(40,calories=Calories,protein=Proteins,\
        carbs=Carbs,fats=Fats)
    # print("This is lunch cal at line 126", lunch_cal) CORRECT
    dinner_cal=lunch_cal
    dinner_protein=lunch_protein
    dinner_carbs=lunch_carbs
    dinner_fats=lunch_fats
    # print("the dinner calories are", dinner_cal)  CORRECT

    temp_cal=breakfast_cal

    find_cal=Food.objects.filter(MealType=1).all()
    sum_cal=0 #This is to be used in finding out total calories of total breakfast 
    #Trying to take out individual macros for foods
    for indv_macros in find_cal:
        # brkfast_carbs =Food.objects.filter(MealType__name__contains='Breakfast')
        brkfast_carbs =Food.objects.filter(carbs__contains='Breakfast')

        # print("First Element of query set is",indv_macros)
        # print("THIS IS THE CARBS WE WERE LOOKING FOR",brkfast_carbs)


    selectedBreakfast = []
    # select_breakfast = Food.objects.filter(MealType__name__contains='Breakfast')
    for var in find_cal:
        Carbohydrates=Food.objects.filter(MealType__name__contains='Breakfast').aggregate(Sum('carbs'))
        Fat=Food.objects.filter(MealType__name__contains='Breakfast').aggregate(Sum('fats'))
        Protein=Food.objects.filter(MealType__name__contains='Breakfast').aggregate(Sum('protien'))
        Grams=Food.objects.filter(MealType__name__contains = 'Lunch').aggregate(Sum('per_how_much_gram'))
        pergrams_breakfast=Grams['per_how_much_gram__sum']
        breakfast_fats = Fat['fats__sum']
        breakfast_carb = Carbohydrates['carbs__sum']
        breakfast_proteins = Protein['protien__sum']
        
        # print("The total carbs are", Carbohydrates)
        break

    # for item in find_cal:
    #     firstcal =macros(carbs = item.carbs, fats = item.fats, proteins = item.protien)
    #     print("first data is ", firstcal)
    #     break
    
    
    #Takes out the calories
    for item in find_cal:
        food_breakfast =macros(carbs = item.carbs, fats = item.fats, proteins = item.protien)
        sum_cal=food_breakfast+sum_cal
        # print("The carbs are is ", carbs)
  
    # from breakfast_protein
    final_protein_calories = breakfast_protein*4
    final_carbs_calories = breakfast_carbs*4
    final_fats_calories = breakfast_fats*4

    final_cal_from_breakfast = final_protein_calories+final_carbs_calories+final_fats_calories
    print("The final calories from breakfast is",final_cal_from_breakfast)

    temp_carbs = 0
    
    # if item.carbs < temp_carbs:

    b_calorie = "{:.2f}".format(sum_cal)

    
        #Have to get sum of food_breakfast
    
    if(sum_cal <= temp_cal):  
        selectedBreakfast.append(item)
        temp_cal = temp_cal - sum_cal
        # print(temp_cal)       
    

    find_lunch=Food.objects.filter(MealType=2).all()
    # sum_cal=0 #This is to be used in finding out total calories of total breakfast 
    selectedLunch = []
    # select_breakfast = Food.objects.filter(MealType__name__contains='Breakfast')
   
    
    
        
        # print("The total carbs are", Carbohydrates)
       
   
    for var in find_lunch:
        Carbohydrates=Food.objects.filter(MealType__name__contains='Lunch').aggregate(Sum('carbs'))
        Fat=Food.objects.filter(MealType__name__contains='Lunch').aggregate(Sum('fats'))
        Protein=Food.objects.filter(MealType__name__contains='Lunch').aggregate(Sum('protien'))
        Grams=Food.objects.filter(MealType__name__contains = 'Lunch').aggregate(Sum('per_how_much_gram'))
        pergrams_lunch=Grams['per_how_much_gram__sum']
        
       
        break
    
    
    final_Lprotein_calories = lunch_protein*4
    final_Lcarbs_calories = lunch_carbs*4
    final_Lfats_calories = lunch_fats*4

    final_cal_from_lunch = int(final_Lprotein_calories+final_Lcarbs_calories+final_Lfats_calories)
    print("The final calories from lunch is",final_cal_from_lunch)
    #Takes out the calories
    for item in find_lunch:
        food_lunch =macros(carbs = item.carbs, fats = item.fats, proteins = item.protien)
        sum_cal=food_lunch+sum_cal

    # print("Sum is",sum_cal)

    
        #Have to get sum of food_breakfast
    
    if(sum_cal <= temp_cal):  
        selectedLunch.append(item)
        temp_cal = temp_cal - sum_cal
        # print(temp_cal)       
   

    find_dinner=Food.objects.filter(MealType=3).all()
    dinner_cal=0 #This is to be used in finding out total calories of total breakfast 
    selectedDinner = []
    # select_breakfast = Food.objects.filter(MealType__name__contains='Breakfast')
    for var in find_dinner:
        Carbohydrates=Food.objects.filter(MealType__name__contains='Dinner').aggregate(Sum('carbs'))
        Fat=Food.objects.filter(MealType__name__contains='Dinner').aggregate(Sum('fats'))
        Protein=Food.objects.filter(MealType__name__contains='Dinner').aggregate(Sum('protien'))
        Grams=Food.objects.filter(MealType__name__contains = 'Lunch').aggregate(Sum('per_how_much_gram'))
        pergrams_dinner=Grams['per_how_much_gram__sum']
        break
    print("The dinner carbs are:",dinner_protein)
    final_Dprotein_calories = dinner_protein*4
    final_Dcarbs_calories = dinner_carbs*4
    final_Dfats_calories = dinner_fats*4

    final_cal_from_Dinner = int(final_Dprotein_calories+final_Dcarbs_calories+final_Dfats_calories)
    print("The final calories from Dinner is",final_cal_from_Dinner)
    
    FINAL_CALCULATED_CALORIES = "{:.2f}".format(final_cal_from_breakfast+final_cal_from_lunch+final_cal_from_Dinner) #CORRECT CALORIES FROM MACROS
    print("The final calories are", FINAL_CALCULATED_CALORIES)

    #Takes out the calories
    for item in find_dinner:
        food_dinner =macros(carbs = item.carbs, fats = item.fats, proteins = item.protien)
        sum_cal=food_dinner+sum_cal
   
        dinner_calories = sum_cal
    
    # print("40% of dinner cal is", dinner_calories)

    
        #Have to get dinner of food_breakfast
    
     
    selectedDinner.append(item)
    temp_cal = temp_cal - sum_cal
    # print("how much iis temp cal now", temp_cal)       
    # else:
    #     print("Else")
        # elif(sum_cal >= temp_cal):
        #     select_breakfast.append(item)
        #     temp_cal = temp_cal - sum_cal
        #     print(temp_cal)  
    # if(temp_cal>=sum):
    #     selectedBreakfast.append([sum])
    #     temp_cal=temp_cal-sum
    # print(selectedBreakfast)

    return render(request, 'main/DietPlan.html',{"breakfast":find_cal,"b_calorie":FINAL_CALCULATED_CALORIES, "lunchs":find_lunch, "lunch_calories": food_lunch, "dinner_calories":food_dinner, "dinner_name":find_dinner,
   'per_grams_breakfast':pergrams_breakfast, 'breakfast_Fats': breakfast_fats, 'breakfast_carbs':breakfast_carb, 'breakfast_proteins':breakfast_proteins, 'per_grams_lunch':pergrams_lunch, 'per_grams_dinner':pergrams_dinner })

def percentage(percentage,**macros):
    return (macros['calories']*percentage)/100,\
        (macros['protein']*percentage)/100,\
        (macros['carbs']*percentage)/100,\
        (macros['fats']*percentage)/100

def macros(**kcal):
    return (kcal['carbs']*4) + (kcal['fats']*9) + (kcal['proteins']*4)