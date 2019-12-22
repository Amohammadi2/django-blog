from django.urls import path
from .views import index, want, addArticle, thanks, deleted, deleteArticle, editArticle, login, signup, logout, changeProfile, showProfile, like, dislike, search, allArticles


urlpatterns = [
    path("", index, name="homepage"),
    path("want/<int:article_id>", want, name="wantarticle"),
    path("addArticle/", addArticle, name="addarticle"),
    path("thanks/", thanks, name="thanks"),
    path("deleteArticle/<int:article_ID>", deleteArticle, name="deletearticle"),
    path("deleted/", deleted, name="deleted"),
    path("editArticle/<int:article_ID>", editArticle, name="editArticle"),
    path("login/", login, name="login"),
    path("signup/", signup, name="signup"),
    path("logout/", logout, name="logout"),
    path('changeProfile/', changeProfile, name="changeprofile"),
    path("showprofile/<int:user_id>", showProfile, name="showprofile"),
    path('likeup/<int:article_id>/', like, name="likeup"),
    path("dislike/<int:article_id>/", dislike, name="dislike"),
    path("search/", search, name="search"),
    path("allArticles/", allArticles, name="allArticles"),
]