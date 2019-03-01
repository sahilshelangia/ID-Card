from django.shortcuts import render
from visitor.models import visitor_detail
from django.core.mail import EmailMultiAlternatives
from django.utils import timezone
from django.urls import reverse
from datetime import datetime
from django.http import HttpResponse
from django.views.generic import View
from utils import render_to_pdf #created in step 4

def index(request):
	return render(request,'visitor/index.html')

def register(request):
	if request.method=="POST":
		name=request.POST['name']
		name_2=request.POST['name_2']
		address=request.POST['address']
		id_no=request.POST['id_no']
		id_type=request.POST['id_type']
		mob=request.POST['mob']
		email=request.POST['email']
		veh=request.POST['veh']
		purpose=request.POST['purpose']
		dest=request.POST['dest']
		pic=request.POST['pic']
		obj=visitor_detail(name=name,name_2=name_2,address=address,id_no=id_no,id_type=id_type,mob=mob,email=email,veh=veh,purpose=purpose,dest=dest,pic=pic)
		obj.save()

		subject, from_email, to = 'Visitor Details at ABV IIITM', 'surjeetsingh41097@gmail.com', email
		text_content = 'This is Visitor ID Card information.'
		html_content = """<p>Welcome to IIITM, your visiting ID is """+ str(obj.id)+""".</p>"""
		msg = EmailMultiAlternatives(subject, text_content, from_email, [to])
		msg.attach_alternative(html_content, "text/html")
		msg.send()
	return render(request,'visitor/new.html')


def list_view(request):
	visitors=visitor_detail.objects.filter(status_in=False)
	context={'visitors':visitors}
	return render(request,'visitor/list.html',context=context)

def detail(request,pk):
	visitor=visitor_detail.objects.get(id=pk)
	context={'visitor':visitor}
	return render(request,'visitor/detail.html',context=context)

def checkedin_list(request):
	visitors=visitor_detail.objects.filter(status_in=True)
	context={'visitors':visitors}
	return render(request,'visitor/list.html',context=context)

def check_out(request,pk):
	visitor=visitor_detail.objects.get(id=pk)
	visitor.time_out=datetime.now()
	visitor.status_in=False
	visitor.save()
	context={'visitor':visitor}
	return render(request,'visitor/detail.html',context=context)

class GeneratePdf(View):
	def get(self, request, *args, **kwargs):
		primary=self.kwargs['pk']
		visitor=visitor_detail.objects.get(pk=primary)
		data={'visitor':visitor}
		pdf = render_to_pdf('visitor/card.html', data)
		return HttpResponse(pdf, content_type='application/pdf')