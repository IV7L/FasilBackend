from django.contrib import admin
from django.urls import path, include
from rest_framework import routers
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
    TokenVerifyView
)

from account.views import (
    AccountViewSet,
    BasicAuthAPIView,
    TeamViewSet,
    SendInvitationView,
    DebateViewersViewSet,
    DebateMemberViewSet,
)
from debate_app.views import (
    DebateViewSet,
    DebateGoalsViewSet,
    DebateCategoryViewSet,
    DebateTimelineViewSet,
)
from debate_app.validation.views import (
    ResourceExternalLinkViewSet,
    ResourceInternalDebatesViewSet,
    ResourceUploadFileViewSet,
    ContractProposalViewSet,
    VoteProposalViewSet,
    DebateArgViewSet,
    DAOArgsViewSet
)
from debate_app.rules.views import (
    CloseDebateRulesViewSet,
    DebateRulesViewSet
)
from debate_app.quote.views import (
    RecessRoomQuoteViewSet,
    DebateQuoteViewSet,
    QuoteBoxCategoryViewSet,
    RecessRoomViewSet,
)

# from django.contrib.auth.models import User, Group
from django.contrib import admin
admin.autodiscover()
router = routers.DefaultRouter()

# Debate register
router.register(r'debates', DebateViewSet)
router.register(r'debate_goals', DebateGoalsViewSet)
router.register(r'debate_category', DebateCategoryViewSet)
router.register(r'debate_timeline', DebateTimelineViewSet)
router.register(r'quotebox_category', QuoteBoxCategoryViewSet)
router.register(r'debate_recessroom', RecessRoomViewSet)
# Validation register
router.register(r'proposals', ContractProposalViewSet)
router.register(r'votes', VoteProposalViewSet)
router.register(r'debate_args', DebateArgViewSet)
router.register(r'dao_args', DAOArgsViewSet)

router.register(r'resource_external', ResourceExternalLinkViewSet)
router.register(r'resource_internal', ResourceInternalDebatesViewSet)
router.register(r'resource_upload', ResourceUploadFileViewSet)
# Rules register
router.register(r'rules_closedebate', CloseDebateRulesViewSet)
router.register(r'rules_debate', DebateRulesViewSet)
# Quote register
router.register(r'quote_recessroom', RecessRoomQuoteViewSet)
router.register(r'quote_debate', DebateQuoteViewSet)
# account process register
router.register(r'accounts', AccountViewSet)
router.register(r'debate_member', DebateMemberViewSet)
router.register(r'debate_viewer', DebateViewersViewSet)
router.register(r'teams', TeamViewSet)

from django.conf import settings
from django.conf.urls.static import static

from django.views.decorators.csrf import csrf_exempt
from rest_framework.authtoken.views import obtain_auth_token
from account.views import EthereumAuthView
urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include(router.urls)),
    path('api-auth/', include('rest_framework.urls')),
        
    path('jwt/api-token-auth/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('jwt/api-token-refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('jwt/api-token-verify/', TokenVerifyView.as_view(), name='token_verify'),

    path('member/send_invitation_mail', SendInvitationView.as_view() ,name='send_invite_mail'),

    path('basicAuth/', BasicAuthAPIView.as_view(), name='basic_auth'),

    path('api-token-auth/', obtain_auth_token, name='api_token_auth'),

    path('ethereum-auth/', EthereumAuthView.as_view(), name='ethereum_auth'),
    
    # path('o/', include('oauth2_provider.urls', namespace='oauth2_provider')),
    # path('users/', UserList.as_view()),
    # path('users/<pk>/', UserDetails.as_view()),
    # path('groups/', GroupList.as_view()),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
