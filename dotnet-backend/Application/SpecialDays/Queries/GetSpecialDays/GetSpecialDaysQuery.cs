using Application.SpecialDays.Models;
using MediatR;
using Microsoft.EntityFrameworkCore;
using Persistence;

namespace Application.SpecialDays.Queries.GetSpecialDays;
public class GetSpecialDaysQuery : IRequest<List<SpecialDayResponseModel>>
{
}

public class GetSpecialDaysQueryHandler(ApplicationDbContext context) : IRequestHandler<GetSpecialDaysQuery, List<SpecialDayResponseModel>>
{
    public async Task<List<SpecialDayResponseModel>> Handle(GetSpecialDaysQuery request, CancellationToken cancellationToken)
    {
        var items = await context.Set<Domain.Entities.SpecialDay>()
        .OrderBy(s=>s.Date)
        .Select(s => new SpecialDayResponseModel{
            Id = s.Id,
            Name = s.Name,
            Date = s.Date,
            Description = s.Description
        }).ToListAsync(cancellationToken);

        return items;
    }
}
