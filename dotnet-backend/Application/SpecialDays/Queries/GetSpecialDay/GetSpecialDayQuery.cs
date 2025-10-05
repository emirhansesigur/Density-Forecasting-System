using Application.SpecialDays.Models;
using MediatR;
using Microsoft.EntityFrameworkCore;
using Persistence;

namespace Application.SpecialDays.Queries.GetSpecialDay;
public class GetSpecialDayQuery : IRequest<SpecialDayResponseModel>
{
    public Guid Id { get; set; }
}
public class GetSpecialDayQueryHandler(ApplicationDbContext context) : IRequestHandler<GetSpecialDayQuery, SpecialDayResponseModel>
{
    public async Task<SpecialDayResponseModel> Handle(GetSpecialDayQuery request, CancellationToken cancellationToken)
    {
        var item = await context.Set<Domain.Entities.SpecialDay>().Select(s => new SpecialDayResponseModel
        {
            Id = s.Id,
            Name = s.Name,
            Date = s.Date,
            Description = s.Description
        }).FirstOrDefaultAsync(x => x.Id == request.Id, cancellationToken: cancellationToken) ?? throw new KeyNotFoundException($"SpecialDay with Id {request.Id} not found.");

        return item;
    }
}
