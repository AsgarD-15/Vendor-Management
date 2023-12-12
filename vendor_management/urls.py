from django.urls import path
from .views import (
    VendorListCreateView, VendorDetailView, VendorPerformanceView,
    PurchaseOrderListCreateView, PurchaseOrderDetailView, PurchaseOrderAcknowledgmentView
)

urlpatterns = [
    path('vendors/', VendorListCreateView.as_view(), name='vendor-list-create'),
    path('vendors/<int:pk>/', VendorDetailView.as_view(), name='vendor-detail'),
    path('vendors/<int:vendor_id>/performance/', VendorPerformanceView.as_view(), name='vendor-performance'),
    path('purchase_orders/', PurchaseOrderListCreateView.as_view(), name='purchaseorder-list-create'),
    path('purchase_orders/<int:pk>/', PurchaseOrderDetailView.as_view(), name='purchaseorder-detail'),
    path('purchase_orders/<int:pk>/acknowledge/', PurchaseOrderAcknowledgmentView.as_view(), name='purchaseorder-acknowledge'),
]
