# views.py
from django.shortcuts import render, redirect
from store.models.address import Address
from store.forms import AddressForm
def save_address(request):
    if request.method == 'POST':
        pincode = request.POST.get('pincode')
        area = request.POST.get('area')
        locality = request.POST.get('locality')
        town = request.POST.get('town')
        village = request.POST.get('village')
        name = request.POST.get('name')
        phone = request.POST.get('phone')
        alt_phone = request.POST.get('alt_phone')

        # Save the address details to the database
        address = Address(
            pincode=pincode,
            area=area,
            locality=locality,
            town=town,
            village=village,
            name=name,
            phone=phone,
            alt_phone=alt_phone
        )
        form = AddressForm(request.POST)
        if form.is_valid():
            address.save()
            # return redirect('success')
    saved_addresses = Address.objects.values('pincode', 'area', 'locality', 'town', 'village', 'name', 'phone', 'alt_phone').distinct()
    return render(request, 'adress.html', {'saved_addresses': saved_addresses})

        # Redirect to a success page or perform any other action

def next_step_view(request):
    if request.method == 'POST':
        selected_address_id = request.POST.get('selected_address_id')
        # Use the selected_address_id as needed, for example:
        selected_address = Address.objects.get(id=selected_address_id)
        
        # Perform any additional logic based on the selected address
    # Render the next step view or redirect as needed
    return render(request, 'next_step.html')