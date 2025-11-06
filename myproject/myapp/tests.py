from django.test import TestCase
import pytest 
from django.urls import reverse, resolve
from django.contrib.auth.models import User
from myapp.models import Item
from myapp.forms import ItemForm
from myapp import views
# Create your tests here.

@pytest.mark.django_db
class TestItemModel():
    def test_item_creation(self):
        item= Item.objects.create(
            title= "new Title",
            description= "this is the desc"
        )
        assert item.title == "new Title"
        assert item.description == "this is the desc"
        assert item.pk is not None
    
    def test_item_string(self):
        item= Item.objects.create(
            title= "new title",
            description= "desc"
        )
        assert str(item)== "new title"
    
    def test_item_ordering(self):
        item1= Item.objects.create(title="t1", description="d1")
        item2= Item.objects.create(title="t2", description="d2")
        item3= Item.objects.create(title="t3", description="d3")

        item= Item.objects.all()
        assert item[0].title =="t3"
        assert item[1].title== "t2"
        assert item[2].title=="t1"
    

@pytest.mark.django_db
class TestItemListView:

    def test_item_list_view(self, client):
        url= reverse('item_list')
        response= client.get(url)
        assert response.status_code ==200
    
    def test_item_list_view_with_item(self, client):
        Item.objects.create(title='t1', description='d1')
        Item.objects.create(title='t2', description='d2')
        url= reverse('item_list')
        response= client.get(url)

        assert response.status_code==200
        assert len(response.context['items'])==2
    
@pytest.mark.django_db
class TestItemCreateView:

    def test_item_create_view(self, client):
        url= reverse('item_create')
        response= client.get(url)
        assert response.status_code== 200
    

    def test_item_create_view_valid(self, client):
        url= reverse('item_create')
        data= {
            'title': 'new title',
            'description': 'new decription'
        }

        response= client.post(url, data)
        assert response.status_code== 302

        assert response.url == reverse('item_list')

        assert Item.objects.count()==1
        item= Item.objects.first()

        assert item.title== 'new title'
    
    def test_item_create_view_invalid(self, client):
        url= reverse('item_create')
        data={
            'title':'',
            'description':'d1'
        }
        response= client.post(url, data)
        assert response.status_code== 200

        assert Item.objects.count()==0

@pytest.mark.django_db
class TestItemDetailView:

    def test_item_read_view(self, client):
        # url= reverse('item_detail')
        item= Item.objects.create(title="t1", description="d1")
        url= reverse('item_detail', args=[item.pk])

        response= client.get(url)
        assert response.status_code==200
        assert response.context['item'].title== "t1"
    
    def test_item_read_view_invalid(self, client):
        url= reverse('item_detail', args=[9999])
        response= client.get(url)
        assert response.status_code== 404

@pytest.mark.django_db
class TestItemUpdateView:

    def test_item_update_view(self, client):
        item= Item.objects.create(
            title="t1", description= "d1"
        )
        url= reverse('item_update', args=[item.pk])
        data={
            'title':'t2',
            'description': 'd2'
        }
        response= client.post(url,data)
        assert response.status_code== 302

        item.refresh_from_db()

        assert item.title=='t2'
        assert item.description=='d2'
    
    def test_item_update_view_invalid(self, client):
        url= reverse('item_update', args=[9999])
        response= client.post(url)
        assert response.status_code== 404

@pytest.mark.django_db
class TestItemDeleteView:
    def test_item_delete_view(self, client):
        item= Item.objects.create(title= "t1", description="d1")
        url= reverse('item_delete', args=[item.pk])
        response = client.post(url)


        assert response.status_code== 302
        assert response.url== reverse('item_list')

        assert Item.objects.count()==0
    
    def test_item_delete_view_invalid(self, client):
        url= reverse('item_delete',args=[9999])
        response= client.post(url)

        assert response.status_code== 404


